# Extract Subtitles from YouTube Videos with OpenAI Whisper and Insanely Fast Whisper

Author : Orhan Cavus
Date   : January 2025

## Download Audio from YouTube

To download audio from a YouTube video, use the following command:

```bash
yt-dlp -x --audio-format mp3 -o "input/video_audio.%(ext)s" <YouTube-URL>
```

Example:

```bash
yt-dlp -x --audio-format mp3 -o "input/video_audio.%(ext)s" https://www.youtube.com/watch?v=0Vjh5d5rez0
```

## Extract Text from Audio with Whisper

Use the following commands to extract text from the downloaded audio using Whisper:

```bash
whisper input/video_audio.mp3 --model medium
whisper input/video_audio.mp3 --model large --language English --output_format srt
whisper input/video_audio.mp3 --model medium --output_format -f {all} --output_dir output
whisper input/video_audio.mp3 --model medium -f all --output_dir output
whisper input/video_audio.mp3 --model medium --task translate -f srt --output_dir output
```

## Extract Text from Audio with Insanely Fast Whisper

For faster transcription, use Insanely Fast Whisper:

[Insanely Fast Whisper GitHub Repository](https://github.com/Vaibhavs10/insanely-fast-whisper)

```bash
insanely-fast-whisper --file-name input/video_audio.mp3 --transcript-path output/output_new.srt --device mps
```

## Installation

Install the required packages with the following commands:

```bash
pip install openai-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

## Additional Links

- [YouTube to Transcript](https://youtubetotranscript.com/)
