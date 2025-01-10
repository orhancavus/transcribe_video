import json
from datetime import timedelta


def json_to_srt(json_file_path):
    """
    Converts a JSON file containing transcription data to SRT format.

    Args:
        json_file_path: Path to the JSON file.

    Returns:
        A string containing the SRT formatted subtitles.
    """

    with open(json_file_path, "r") as f:
        data = json.load(f)

    srt_lines = []
    for i, chunk in enumerate(data["chunks"]):
        start_time = timedelta(seconds=chunk["timestamp"][0])
        end_time = timedelta(seconds=chunk["timestamp"][1])

        start_time_str = (
            str(start_time).replace(".", ",")
            if "." in str(start_time)
            else str(start_time) + ",000000"
        )
        end_time_str = (
            str(end_time).replace(".", ",")
            if "." in str(start_time)
            else str(start_time) + ",990000"
        )
        srt_lines.append(str(i + 1))
        srt_lines.append(f"{start_time_str} --> {end_time_str}")
        srt_lines.append(chunk["text"].strip())
        srt_lines.append("")  # Empty line between subtitles

    return "\n".join(srt_lines)


def save_srt_from_json(json_file_path, srt_file_path):
    """
    Converts a JSON file containing transcription data to SRT format and saves it to a file.

    Args:
        json_file_path: Path to the JSON file.
        srt_file_path: Path to the output SRT file.
    """
    srt_content = json_to_srt(json_file_path)
    with open(srt_file_path, "w") as f:
        f.write(srt_content)


if __name__ == "__main__":
    # Example usage:
    json_file = (
        "input_subs/Ujas1984_1989.json"  # Replace with the path to the input JSON file
    )
    srt_file = (
        "output/Ujas1984_1989.srt"  # Replace with the path to the output SRT file
    )
    save_srt_from_json(json_file, srt_file)
