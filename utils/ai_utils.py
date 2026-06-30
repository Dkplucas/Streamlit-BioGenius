"""
AI integration utilities for Openrouter API.
"""
import requests
from typing import List, Dict, Any
import os


SYSTEM_PROMPT = """You are an expert bioinformatics teacher and scientist. Your role is to:
1. Explain bioinformatics concepts clearly and accurately
2. Analyze biological sequences and interpret results
3. Answer student questions about genetics, genomics, and molecular biology
4. Provide scientifically accurate information in simple, understandable language
5. Avoid hallucinations and cite biological principles when explaining

When analyzing sequences:
- Interpret GC content (high GC = thermostable, found in certain organisms)
- Explain nucleotide composition
- Suggest biological significance of sequence properties

Keep responses concise, educational, and accurate."""


def create_openrouter_message(
    api_key: str,
    messages: List[Dict[str, str]],
    model: str = "openrouter/auto"
) -> Dict[str, Any]:
    """
    Send request to Openrouter API and get response.

    Args:
        api_key: Openrouter API key
        messages: List of message dictionaries with 'role' and 'content'
        model: Model to use (default: openrouter/auto)

    Returns:
        Dict with response data or error
    """
    if not api_key:
        return {
            "error": True,
            "message": "API key not configured. Please set OPENROUTER_API_KEY environment variable."
        }

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Bioinformatics Assistant"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return {
                "error": False,
                "response": data["choices"][0]["message"]["content"],
                "model": data.get("model", "unknown")
            }
        else:
            return {
                "error": True,
                "message": "Invalid response from API"
            }

    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "API request timed out. Please try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Connection error. Please check your internet connection."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": True,
            "message": f"API Error: {str(e)}"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Error: {str(e)}"
        }


def format_sequence_analysis_context(analysis: Dict[str, Any]) -> str:
    """
    Format sequence analysis results into optimized text context.
    Includes only essential information to reduce token usage.
    """
    if not analysis:
        return ""

    context = f"Analysis: {analysis.get('total_sequences', 0)} sequences, "
    context += f"{analysis.get('total_length', 0)} bp total, "
    context += f"{analysis.get('average_length', 0)} bp avg, "
    context += f"{analysis.get('average_gc_content', 0)}% GC"

    if analysis.get('sequences') and len(analysis['sequences']) > 0:
        context += "\nSequences: "
        seq_summaries = []
        for seq in analysis['sequences'][:3]:
            summary = f"{seq.get('header', 'Unknown')[:30]}({seq.get('length', 0)}bp, {seq.get('gc_content', 0)}%GC)"
            seq_summaries.append(summary)
        context += ", ".join(seq_summaries)

    return context


def chat_with_bioinformatics_ai(
    api_key: str,
    user_query: str,
    chat_history: List[Dict[str, str]] = None,
    sequence_context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Main function to chat with AI about bioinformatics.

    Args:
        api_key: Openrouter API key
        user_query: User's question
        chat_history: Previous messages for context (last 3-5)
        sequence_context: Analysis results if user asked about sequences

    Returns:
        Dict with response and metadata
    """
    if chat_history is None:
        chat_history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in chat_history[-5:]:
        messages.append(msg)

    query_with_context = user_query
    if sequence_context:
        context = format_sequence_analysis_context(sequence_context)
        query_with_context = f"{user_query}\n\n{context}"

    messages.append({"role": "user", "content": query_with_context})

    result = create_openrouter_message(api_key, messages)

    return result
