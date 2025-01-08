# Extract Video subtitiles to files with Open AI whisper

## Download audio from youtube video

```bash
yt-dlp -x --audio-format mp3 -o "input/video_audio.%(ext)s" <YouTube-URL>
yt-dlp -x --audio-format mp3 -o "input/video_audio.%(ext)s" https://www.youtube.com/watch?v=0Vjh5d5rez0
```

## Extract text from audio with wisper command prompt examples

```bash
whisper input/video_audio.mp3 --model medium
whisper input/video_audio.mp3 --model large --language English --output_format srt
whisper input/video_audio.mp3 --model medium --output_format -f {all} --output_dir output
whisper input/video_audio.mp3 --model medium -f all --output_dir output
whisper input/video_audio.mp3 --model medium --task translate -f srt --output_dir output
```

## Extract text from audio with insanely-fast-whisper command prompt examples

[Insanely Fast whisper https://github.com/Vaibhavs10/insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)

```bash
insanely-fast-whisper --file-name input/video_audio.mp3 --transcript-path output/output_new.srt --device mps
```

## Installation

```bash
pip install openai-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

## Additonal Links

[Yotube transcribe https://youtubetotranscript.com/](https://youtubetotranscript.com/)
