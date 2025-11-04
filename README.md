# Transcribe YouTube Audio

This script downloads audio from a YouTube video and transcribes it using different methods.
Note : Be sure to be logged in with youtube account in Safari for Mac OS!!

Author : Orhan Cavus  
Date   : January 2025  

## Requirements

- Python 3.x
- `yt-dlp`
- `whisper`
- `insanely-fast-whisper`
- `subtitels2srt`

## Installation

Install the required Python packages:

```bash
pip install whisper argparse
```

Install `yt-dlp`:

```bash
pip install yt-dlp
```

Install `insanely-fast-whisper`:

```bash
pip install insanely-fast-whisper
```

## Usage

### Command Line Arguments

- `--youtube_url`: URL of the YouTube video to transcribe.
- `--file_name`: Base name for the downloaded audio file.
- `--method`: Transcription method to use: `whisper`, `fast_whisper`, or `whisper_lib`.
- `--task`: Task for `fast_whisper` method: `transcribe`, `translate`, or `run_main`.

### Example

```bash
python transcribe_youtube.py --youtube_url "https://www.youtube.com/watch?v=example" --file_name "example_audio" --method "fast_whisper" --task "transcribe"
```

## Functions

- `download_audio(youtube_url, output_file)`: Downloads audio from a YouTube video.
- `transcribe_audio_whisper(audio_file, model="medium")`: Transcribes audio using Whisper.
- `transcribe_audio2srt_fast_whisper(audio_file, model="openai/whisper-large-v3", task="transcribe")`: Transcribes audio using Insanely Fast Whisper and saves as SRT.
- `transcribe_audio_whisper_lib(audio_file, model="medium")`: Transcribes audio using Whisper library.
- `get_command_args()`: Parses command line arguments.
- `process_args(args)`: Processes command line arguments and performs the transcription.
- `dowload_transcribe(url, file_name)`: Downloads and transcribes audio.
- `run_custom()`: Custom function for downloading and transcribing audio.

## License

This project is licensed under the MIT License.
