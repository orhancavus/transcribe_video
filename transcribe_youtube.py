import os
import whisper
import argparse
from subtitels2srt import save_srt_from_json


# Step 1: Download YouTube audio
def download_audio(youtube_url, output_file):
    system_script = f'yt-dlp -x --audio-format mp3 -o "{output_file}" {youtube_url}'
    print(f"{system_script=}")
    os.system(system_script)


# Step 2: Transcribe with Whisper
def transcribe_audio_whisper(audio_file, model="medium"):
    system_script = (
        f"whisper input/{audio_file} --model {model} -f all --output_dir output"
    )
    print(f"{system_script=}")
    os.system(system_script)


# Step 2: Transcribe with Whisper
def transcribe_audio2srt_fast_whisper(
    audio_file, model="openai/whisper-large-v3", task="transcribe"
):
    audio_file_base = os.path.splitext(audio_file)[0]

    json_file = f"output/{audio_file_base}.json"
    system_script = f"insanely-fast-whisper --file-name input/{audio_file} --model {model} --task {task} --transcript-path {json_file} --device mps"

    print(f"System script :{system_script}")
    os.system(system_script)

    output_srt_file = f"output/{audio_file_base}.srt"
    save_srt_from_json(json_file, output_srt_file)


def transcribe_audio_whisper_lib(audio_file, model="medium"):
    # Ensure MPS is used for general operations but fall back to CPU for sparse tensors
    # device = "mps" if torch.backends.mps.is_available() else "cpu"
    device = "cpu"
    # Load the model
    model = whisper.load_model(model, device=device)

    # Transcribe audio
    result = model.transcribe(audio_file, verbose=True)
    return result["text"]


def args():
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube audio using different methods."
    )
    parser.add_argument(
        "youtube_url", type=str, help="URL of the YouTube video to transcribe"
    )
    parser.add_argument(
        "file_name", type=str, help="Base name for the downloaded audio file"
    )
    parser.add_argument(
        "method",
        type=str,
        choices=["whisper", "fast_whisper", "whisper_lib"],
        help="Transcription method to use: 'whisper', 'fast_whisper', or 'whisper_lib'",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="transcribe",
        help="Task for fast_whisper method: 'transcribe' or 'translate'",
    )
    args = parser.parse_args()

    file_name_mp3 = f"{args.file_name}.mp3"

    print(f"Downloading audio... {args.youtube_url}")
    download_audio(args.youtube_url, file_name_mp3)

    print(f"Transcribing audio... {file_name_mp3}")
    if args.method == "whisper":
        transcribe_audio_whisper(file_name_mp3)
    elif args.method == "fast_whisper":
        transcribe_audio2srt_fast_whisper(file_name_mp3, task=args.task)
    elif args.method == "whisper_lib":
        transcription = transcribe_audio_whisper_lib(file_name_mp3)
        with open(f"output/{args.file_name}.txt", "w") as f:
            f.write(transcription)

    print("Transcription complete!")


def run_custom():
    # youtube_url = "https://www.youtube.com/watch?v=0Vjh5d5rez0"
    # file_name = "video_audio"
    # youtube_url = "https://www.youtube.com/watch?v=mjwgy3nzIlI&t=2s"
    youtube_url = "https://www.youtube.com/watch?v=k6RLAsTeIJc&list=PL-CsGB9XKEpRuPPrUplJzrlQ9f5O8bxz7&index=5"
    file_name = "Bulgaria1984"
    file_name_mp3 = f"{file_name}.mp3"

    if False:
        print(f"Downloading audio... {youtube_url}")
        download_audio(youtube_url, file_name_mp3)
        # transcribe_audio_whisper(file_name)

    if True:
        print(f"Transcribing audio... {file_name_mp3}")
        # transcribe_audio_whisper_lib(file_name_mp3)
        # print("Transcription complete!")
        transcribe_audio2srt_fast_whisper(file_name_mp3, task="translate")


if __name__ == "__main__":
    # args()
    # exit()
    run_custom()
