"""
detector.py
-----------
AI text detection module using a RoBERTa-based classifier.
Scores input text on a 0-1 scale where 1 = AI-generated, 0 = Human-written.
Also used sentence-by-sentence for highlighting in the UI.
"""

import os
import warnings

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Detection threshold — lowered from default 0.5 to improve sensitivity
# to modern AI writing patterns (model trained on GPT-2 era text)
THRESHOLD = 0.35

try:
    model_name = "roberta-base-openai-detector"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()
    _model_loaded = True
except Exception as e:
    print(f"[detector] Could not load model — {e}")
    _model_loaded = False


def detect_ai_text(text: str) -> dict:
    """
    Detect whether the given text is AI-generated or human-written.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: {
            "score" (float): AI likelihood score between 0.0 and 1.0,
            "label" (str): "AI-generated" or "Human-written"
        }
    """
    if not text or not text.strip():
        return {"score": 0.0, "label": "Human-written"}

    if not _model_loaded:
        return {"score": 0.0, "label": "Model not loaded — run: pip install transformers torch"}

    # Tokenize and run inference
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs  = torch.softmax(logits, dim=-1)[0]

    # Find the FAKE label index (AI-generated) from the model's label map
    fake_idx = None
    for idx, name in model.config.id2label.items():
        if name.upper() == "FAKE":
            fake_idx = idx
            break

    # Use FAKE probability as AI score; fallback to index 1 if label not found
    if fake_idx is not None:
        ai_score = round(probs[fake_idx].item(), 2)
    else:
        ai_score = round(probs[1].item(), 2)

    label = "AI-generated" if ai_score > THRESHOLD else "Human-written"

    return {"score": ai_score, "label": label}