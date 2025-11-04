#!/usr/bin/env python3
import os
import argparse
import pysrt

"""This script extracts plain text from .srt subtitle files and writes the extracted text to .txt files.
It can process a single .srt file or recursively search a folder for .srt files.

Functions:
  extract_text_with_pysrt(srt_file):

  write_text_to_file(text, output_file):

  extract_text_from_srt_files(folder_path):
    and extracts subtitles using the extract_text_with_pysrt() function.

Usage:
  Run the script with the --file argument to process a single .srt file or with the --folder argument to process all .srt files in a folder.
"""


def extract_text_with_plain_reading(srt_file):
    """
    Extracts plain text from a .srt file using plain file reading operations.

    Args:
      srt_file: Path to the .srt file.

    Returns:
      A string containing the extracted plain text.
    """
    with open(srt_file, "r") as file:
        lines = file.readlines()

    plain_text = ""
    total_lines = 0
    for line in lines:
        if not line.strip().isdigit() and "-->" not in line:
            plain_text += line.strip() + " "
            total_lines += 1
    print(f"Total lines: {total_lines}")

    return plain_text.strip()


def extract_text_with_pysrt(srt_file):
    """
    Extracts plain text from a .srt file using the pysrt library.

    Args:
      srt_file: Path to the .srt file.

    Returns:
      A string containing the extracted plain text.
    """
    subs = pysrt.open(srt_file, error_handling=pysrt.ERROR_RAISE)
    plain_text = " ".join([sub.text for sub in subs])
    return plain_text


def write_text_to_file(text, output_file):
    """
    Writes the given text to a file.

    Args:
      text: The text to write to the file.
      output_file: Path to the output file.
    """
    with open(output_file, "w") as f:
        f.write(text)


def extract_text_from_srt_files(folder_path):
    """
    Recursively searches the given folder and its subfolders for .srt files
    and extracts subtitles using the extract_text() function.

    Args:
      folder_path: Path to the folder to search for .srt files.

    Returns:
      A dictionary where keys are file paths and values are the extracted text.
    """
    extracted_texts = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".srt"):
                file_path = os.path.join(root, file)
                extracted_text = extract_text_with_plain_reading(file_path)
                extracted_texts[file_path] = extracted_text

    return extracted_texts


def extraxct_srt_to_text(file_path):
    extracted_text = extract_text_with_plain_reading(file_path)
    output_file = os.path.join(
        os.path.dirname(file_path),
        os.path.basename(file_path).replace(".srt", ".txt"),
    )
    write_text_to_file(extracted_text, output_file)


if __name__ == "__main__":
    # python subtitles2text.py --file /Users/orhancavus/Development/Python/local_projects/llm_agents/transcribe_video/output/archive/OpitzaAsimilatsia1984_1989/OpitzaAsimilatsia1984_1989_en.srt
    # python subtitles2text.py --folder output/archive

    parser = argparse.ArgumentParser(description="Extract text from subtitle files.")
    parser.add_argument("--file", type=str, help="Path to the subtitle file.")
    parser.add_argument(
        "--folder", type=str, help="Path to the folder containing subtitle files."
    )
    args = parser.parse_args()

    if args.file:
        extraxct_srt_to_text(args.file)

    if args.folder:
        extracted_texts = extract_text_from_srt_files(args.folder)
        for file_path, text in extracted_texts.items():
            print(f"Extracted text from {file_path}")
            output_file = os.path.join(
                os.path.dirname(file_path),
                os.path.basename(file_path).replace(".srt", ".txt"),
            )
            write_text_to_file(text, output_file)
