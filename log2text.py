def extract_text(text_file):
    """
    Extracts plain text from a file containing subtitles in the following format:

    "[05:31.640 --> 05:35.200]  boosts collaboration and creativity."

    Args:
      text_file: Path to the text file containing subtitles.

    Returns:
      A string containing the extracted plain text.
    """

    with open(text_file, "r") as f:
        lines = f.readlines()

    plain_text = ""
    for line in lines:
        # Split the line by the first occurrence of ']'
        parts = line.split("]", 1)
        if len(parts) > 1:  # Ensure there is text after the timestamp
            plain_text += parts[1].strip() + " "

    return plain_text


# Example usage:
file_path = "output/video_audio.txt"  # Replace with the actual file path
extracted_text = extract_text(file_path)
print(f"Extracted text{extracted_text}")
