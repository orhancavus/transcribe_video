import mlx_whisper


def transcribe():
    print("Transcribing...")
    text = mlx_whisper.transcribe(
        "input/video_audio.mp3",
        verbose=True,
    )["text"]

    with open("input/imeto.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Transcription saved to input/video_audio_mlx_code.txt")


if __name__ == "__main__":
    transcribe()
