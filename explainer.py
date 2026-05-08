import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_explanation(text, score):

    prompt = f"""
    A text has received an AI detection score of {score}.

    Text:
    "{text}"

    Explain in plain English why this text may appear AI-generated.
    Keep explanation short and beginner-friendly.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    explanation = response.choices[0].message.content

    return explanation