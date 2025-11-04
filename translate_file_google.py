#!/usr/bin/env python3
import argparse
from deep_translator import GoogleTranslator
from pathlib import Path

CHUNK_SIZE = 5000  # Google Translate limit per request

def chunk_text(text: str, max_size: int = CHUNK_SIZE):
    """Split text into chunks of up to `max_size` characters without cutting lines mid-way."""
    chunks = []
    current = []
    current_len = 0

    for line in text.splitlines(True):  # keep newline chars
        if current_len + len(line) > max_size:
            chunks.append(''.join(current))
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line)

    if current:
        chunks.append(''.join(current))
    return chunks

def translate_file(input_path: str, output_path: str, source_lang: str, target_lang: str):
    input_file = Path(input_path)
    output_file = Path(output_path)

    text = input_file.read_text(encoding="utf-8")

    translator = GoogleTranslator(source=source_lang, target=target_lang)

    chunks = chunk_text(text)
    translated_chunks = []

    print(f"📘 Translating {len(chunks)} chunks...")

    for i, chunk in enumerate(chunks, start=1):
        print(f"  → Chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        translated = translator.translate(chunk)
        translated_chunks.append(translated)

    full_translation = "\n".join(translated_chunks)
    output_file.write_text(full_translation, encoding="utf-8")

    print(f"\n✅ Translation complete! From {source_lang} → {target_lang}")
    print(f"📁 Saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Translate a text file using GoogleTranslator (deep-translator) in chunks.")
    parser.add_argument("input", help="Path to input text file")
    parser.add_argument("-o", "--output", default="translated.txt", help="Output file path")
    parser.add_argument("-s", "--source", default="auto", help="Source language (default: auto-detect)")
    parser.add_argument("-t", "--target", default="en", help="Target language (default: English)")

    args = parser.parse_args()
    translate_file(args.input, args.output, args.source, args.target)

if __name__ == "__main__":
    main()
