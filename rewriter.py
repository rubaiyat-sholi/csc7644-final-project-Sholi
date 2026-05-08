import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_rewrite(text, score):

    prompt = f"""You are helping someone make their writing sound less AI-generated.

The following text scored {score} on an AI detector (higher = more AI-like):

"{text}"

Rewrite it so it sounds like a real person wrote it. Follow these rules strictly:
- Use casual, conversational language like you're explaining to a friend
- Add small imperfections — contractions, informal phrasing, personal tone
- Avoid formal words like "facilitate", "utilize", "enable", "leverage", "landscape"
- Avoid long structured sentences — break them up
- Do NOT use bullet points or lists
- Do NOT start with "Here is" or "Certainly"
- Just return the rewritten text only, nothing else

Rewritten text:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1.2
    )

    suggestion = response.choices[0].message.content.strip()

    return suggestion