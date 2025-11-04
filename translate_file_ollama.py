#!/usr/bin/env python3
import argparse
import time
import json
from pathlib import Path
import requests
from typing import List

DEFAULT_ENDPOINT = "http://localhost:11434"
DEFAULT_MODEL = "gpt-oss:20b"  # change to a model you have
# Keep chunks modest so the model has room for output under token limits
DEFAULT_CHUNK_SIZE = 3500

SYSTEM_PROMPT = (
    "You are a precise, context-aware translator. "
    "Task: Translate the user's text into the requested target language.\n\n"
    "Requirements:\n"
    "• Translate meaning faithfully; keep tone and register.\n"
    "• Preserve formatting, markdown, line breaks, code blocks, and inline markup.\n"
    "• Do NOT add explanations, summaries, headings, or extra text.\n"
    "• If the text includes code or commands, keep them unchanged unless they're natural language.\n"
    "• Keep placeholders, variables, and tags intact.\n"
)

USER_PROMPT_TEMPLATE = (
    "Target language: {target_lang}\n"
    "{source_hint}"
    "Translate the following content. Return ONLY the translated text:\n\n"
    "<source>\n{content}\n</source>"
)

def chunk_text(text: str, max_size: int) -> List[str]:
    """Split text into chunks up to max_size without breaking lines."""
    chunks, buf, length = [], [], 0
    for line in text.splitlines(True):  # keep newlines
        if length + len(line) > max_size and buf:
            chunks.append(''.join(buf))
            buf, length = [line], len(line)
        else:
            buf.append(line)
            length += len(line)
    if buf:
        chunks.append(''.join(buf))
    return chunks

def ollama_chat(endpoint: str, model: str, system: str, user: str, temperature: float = 0.2, retries: int = 3, timeout: int = 120) -> str:
    """
    Call Ollama's /api/chat (native) endpoint with a system + user message.
    """
    url = endpoint.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {
            "temperature": temperature
        },
    }

    backoff = 1.0
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            # Expected shape: {"message":{"role":"assistant","content":"..."}, ...}
            msg = data.get("message", {}).get("content")
            if not isinstance(msg, str):
                raise ValueError(f"Unexpected response: {json.dumps(data)[:500]}")
            return msg
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(backoff)
            backoff *= 2
    # Should never reach here
    return ""

def translate_file(
    input_path: str,
    output_path: str,
    target_lang: str,
    source_lang: str = "auto",
    model: str = DEFAULT_MODEL,
    endpoint: str = DEFAULT_ENDPOINT,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    temperature: float = 0.2,
):
    in_file = Path(input_path)
    out_file = Path(output_path)
    text = in_file.read_text(encoding="utf-8")

    chunks = chunk_text(text, chunk_size)
    print(f"📘 Translating {len(chunks)} chunk(s) with model '{model}' at {endpoint} …")
    print(f"   Target: {target_lang} | Source: {source_lang}")

    translated_parts: List[str] = []

    source_hint = "" if source_lang.lower() == "auto" else f"Source language: {source_lang}\n"
    for i, chunk in enumerate(chunks, 1):
        user_prompt = USER_PROMPT_TEMPLATE.format(
            target_lang=target_lang,
            source_hint=source_hint,
            content=chunk
        )
        print(f"  → Chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        translated = ollama_chat(
            endpoint=endpoint,
            model=model,
            system=SYSTEM_PROMPT,
            user=user_prompt,
            temperature=temperature,
        )
        translated_parts.append(translated)

    result = "".join(translated_parts)
    out_file.write_text(result, encoding="utf-8")
    print(f"\n✅ Done! Saved to: {out_file}")

def main():
    ap = argparse.ArgumentParser(
        description="Translate a text file using a local LLM via Ollama REST."
    )
    ap.add_argument("input", help="Path to input text file (UTF-8)")
    ap.add_argument("-o", "--output", default="translated.txt", help="Output file path")
    ap.add_argument("-t", "--target", default="en", help="Target language (e.g., en, tr, de)")
    ap.add_argument("-s", "--source", default="auto", help='Source language or "auto"')
    ap.add_argument("-m", "--model", default=DEFAULT_MODEL, help="Ollama model name")
    ap.add_argument("-e", "--endpoint", default=DEFAULT_ENDPOINT, help="Ollama base URL")
    ap.add_argument("-c", "--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Max characters per chunk")
    ap.add_argument("--temp", type=float, default=0.2, help="Temperature (0–1)")

    args = ap.parse_args()

    translate_file(
        input_path=args.input,
        output_path=args.output,
        target_lang=args.target,
        source_lang=args.source,
        model=args.model,
        endpoint=args.endpoint,
        chunk_size=args.chunk_size,
        temperature=args.temp,
    )

if __name__ == "__main__":
    main()
