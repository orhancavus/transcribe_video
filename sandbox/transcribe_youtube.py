import logging
import os
import sys
import whisper
import argparse
import subprocess

from json2srt import save_srt_from_json
from srt2text import extraxct_srt_to_text


def setup_logging():
    logging.basicConfig(
        filename="app.log",  # File to store logs
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# Step 1: Download YouTube audio
def download_audio(youtube_url, output_file):
    output_path = f"input/{output_file}"
    logger.info(f"Downloading audio from {youtube_url} to {output_path}")

    if not os.path.exists(output_path):
        # Ensure the "input" directory exists
        os.makedirs("input", exist_ok=True)

        system_script = [
            "yt-dlp",
            "-x",
            "--abort-on-error",
            "--audio-format",
            "mp3",
            "-o",
            output_path,
            youtube_url,
        ]
        print(f"Executing: {' '.join(system_script)}")

        # Run the command and wait until it finishes
        try:
            subprocess.run(system_script, check=True)
            print(f"Download completed: {output_path}")
            logger.info(f"Downloaded audio from {youtube_url} to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading audio from {youtube_url}: {e}")
            print(f"An error occurred while downloading: {e}")
            # Re-raise so callers can decide to exit
            raise
    else:
        print(f"File {output_path} already exists. Skipping download.")
        logger.info(f"File exists, skipped download: {output_path}")
        return output_path


# Step 2: Transcribe with Whisper
def transcribe_audio_whisper(audio_file, model="medium"):
    logger.info(f"Transcribing audio with Whisper: {audio_file}")
    system_script = (
        f"whisper input/{audio_file} --model {model} -f all --output_dir output"
    )
    print(f"{system_script=}")
    os.system(system_script)


# Step 2: Transcribe with Whisper
def transcribe_audio2srt_fast_whisper(
    audio_file, model="openai/whisper-large-v3", task="transcribe"
):
    logger.info(f"Transcribing audio with Fast Whisper: {audio_file}")
    audio_file_base = os.path.splitext(audio_file)[0]

    json_file = f"output/{audio_file_base}.json"
    system_script = f"insanely-fast-whisper --file-name input/{audio_file} --model {model} --task {task} --transcript-path {json_file} --device mps"

    print(f"System script :{system_script}")
    os.system(system_script)

    output_srt_file = f"output/{audio_file_base}.srt"
    logger.info(f"Saving SRT to {output_srt_file}")
    save_srt_from_json(json_file, output_srt_file)

    if os.path.exists(json_file):
        os.remove(json_file)
        logger.info(f"Deleted file: {json_file}")
    else:
        print(f"File not found: {json_file}")

    logger.info(f"Extracting text from SRT file: {output_srt_file}")
    extraxct_srt_to_text(output_srt_file)


def transcribe_audio_whisper_lib(audio_file, model="medium"):
    # Ensure MPS is used for general operations but fall back to CPU for sparse tensors
    # device = "mps" if torch.backends.mps.is_available() else "cpu"
    device = "cpu"
    # Load the model
    logger.info(f"Loading Whisper model: {model}")
    model = whisper.load_model(model, device=device)

    # Transcribe audio
    result = model.transcribe(audio_file, verbose=True)
    return result["text"]


def get_command_args():
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube audio using different methods."
    )
    parser.add_argument(
        "--youtube_url", type=str, help="URL of the YouTube video to transcribe"
    )
    parser.add_argument(
        "--file_name", type=str, help="Base name for the downloaded audio file"
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["whisper", "fast_whisper", "whisper_lib"],
        help="Transcription method to use: 'whisper', 'fast_whisper', or 'whisper_lib'",
    )
    parser.add_argument(
        "--task",
        type=str,
        choices=["transcribe", "translate", "run_main", "custom"],
        default="transcribe",
        help="Task for fast_whisper method: 'transcribe' or 'translate'",
    )
    args = parser.parse_args()

    if not args.youtube_url or not args.file_name or not args.method:
        print("ARGS:", args.youtube_url, args.file_name, args.method, args.task)
        parser.print_help()
        parser.exit()

    return args


def process_args(args):
    file_name_mp3 = f"{args.file_name}.mp3"

    print(f"Downloading audio... {args.youtube_url}")
    try:
        download_audio(args.youtube_url, file_name_mp3)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        print(f"Download failed: {e}")
        print(
            "Note : Be sure to be logged in with youtube account in Safari for Mac OS!!"
        )
        sys.exit(1)

    print(f"Transcribing audio... {file_name_mp3}")
    if args.method == "whisper":
        transcribe_audio_whisper(file_name_mp3)
    elif args.method == "fast_whisper":
        transcribe_audio2srt_fast_whisper(file_name_mp3, task=args.task)
    elif args.method == "whisper_lib":
        transcription = transcribe_audio_whisper_lib(file_name_mp3)
        with open(f"output/{args.file_name}.txt", "w") as f:
            f.write(transcription)

    # Delete the mp3 file after transcription
    if os.path.exists(f"input/{file_name_mp3}"):
        os.remove(f"input/{file_name_mp3}")
        print(f"Deleted file: input/{file_name_mp3}")
    else:
        print(f"File not found: input/{file_name_mp3}")

    print("Transcription complete!")


def dowload_transcribe(url, file_name):
    file_name_mp3 = f"{file_name}.mp3"

    print(f"Downloading audio... {url}")
    try:
        download_audio(url, file_name_mp3)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        print(f"Download failed: {e}")
        print(
            "\n\nNote : Be sure to be logged in with youtube account in Safari for Mac OS!!"
        )
        sys.exit(1)

    print(f"Transcribing audio... {file_name_mp3}")
    try:
        transcribe_audio2srt_fast_whisper(file_name_mp3, task="translate")
        print("Transcription complete!")
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        print(f"Transcription failed: {e}")


def run_custom():
    # youtube_url = "https://www.youtube.com/watch?v=0Vjh5d5rez0"
    # file_name = "video_audio"
    # youtube_url = "https://www.youtube.com/watch?v=mjwgy3nzIlI&t=2s"
    # youtube_url = "https://www.youtube.com/watch?v=k6RLAsTeIJc&list=PL-CsGB9XKEpRuPPrUplJzrlQ9f5O8bxz7&index=5"
    youtube_url = "https://www.youtube.com/watch?v=1cD6tuFAPMo&list=PL-CsGB9XKEpRuPPrUplJzrlQ9f5O8bxz7"
    file_name = "video_audio"
    file_name_mp3 = f"{file_name}.mp3"

    function_to_use = (
        "transcribe"  # Change this to `"download"` to download the audio from YouTube,
    )
    if function_to_use == "download":
        print(f"Downloading audio... {youtube_url}")
        try:
            download_audio(youtube_url, file_name_mp3)
        except Exception as e:
            logger.error(f"Download failed: {e}")
            print(f"Download failed: {e}")
            print(
                "\n\nNote : Be sure to be logged in with youtube account in Safari for Mac OS!!"
            )
            sys.exit(1)
        # transcribe_audio_whisper(file_name)
    elif function_to_use == "transcribe":
        print(f"Transcribing audio... {file_name_mp3}")
        # transcribe_audio_whisper_lib(file_name_mp3)
        # print("Transcription complete!")
        transcribe_audio2srt_fast_whisper(file_name_mp3, task="translate")
    else:
        print("No function to run")


if __name__ == "__main__":
    args = get_command_args()
    # exit()
    # run_custom()

    logger.info(f"Arguments: {args}")

    if args.task == "run_main":
        url = "https://www.youtube.com/watch?v=NkWV4Q9z_-E&list=PL-CsGB9XKEpRuPPrUplJzrlQ9f5O8bxz7&index=7"
        file_name = "Ujas1984_1989"
        dowload_transcribe(url=url, file_name=file_name)
    elif args.task == "custom":
        run_custom()
    else:
        # task transcribe or translate
        process_args(args)

    logger.info("Finished!")
