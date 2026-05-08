import time
import json

from detector import detect_ai_text
from explainer import generate_explanation
from rewriter import generate_rewrite

print("=== Explainable AI Text Detection Assistant ===\n")

text = input("Enter text: ")

print("\n[Agent] Step 1: Calling detection tool...")
time.sleep(1)

# Step 1: Detection
result = detect_ai_text(text)

print("[Agent] Step 2: Generating explanation...")
time.sleep(1)

# Step 2: Explanation
explanation = generate_explanation(text, result["score"])

print("[Agent] Step 3: Generating rewrite suggestion...")
time.sleep(1)

# Step 3: Rewrite
suggestion = generate_rewrite(text, result["score"])

# Final structured output
final_output = {
    "input_text": text,
    "ai_score": result["score"],
    "label": result["label"],
    "explanation": explanation,
    "rewrite_suggestion": suggestion
}

print("\n--- FINAL RESULT ---")

# Pretty JSON format
print(json.dumps(final_output, indent=4))