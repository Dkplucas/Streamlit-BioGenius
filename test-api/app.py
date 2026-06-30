import os
import requests

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-fable-5"

dna_sequence = (
    "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
)

prompt = f"""
You are an expert molecular biologist.

Analyze the following DNA sequence and provide:
1. A brief description of the sequence.
2. Any notable sequence features (e.g. ORFs, GC content, motifs if apparent).
3. Whether it appears to encode a protein.
4. Any limitations of interpreting this sequence without additional context.

DNA sequence:
{dna_sequence}
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are an expert in molecular biology and genomics. "
                "Provide scientifically accurate interpretations and clearly "
                "state any uncertainty."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
    "temperature": 0.2,
    "max_tokens": 800,
}

response = requests.post(
    API_URL,
    headers=headers,
    json=payload,
    timeout=60,
)

response.raise_for_status()

result = response.json()

# OpenAI-compatible response format
analysis = result["choices"][0]["message"]["content"]

print(analysis)