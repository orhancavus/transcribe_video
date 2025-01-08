import os
import whisper
from subtitels2srt import save_srt_from_json


# Step 1: Download YouTube audio
def download_audio(youtube_url, output_file):
    system_script = 'yt-dlp -x --audio-format mp3 -o "{output_file}" {youtube_url}'
    print(system_script)
    os.system(system_script)


# Step 2: Transcribe with Whisper
def transcribe_audio_whisper(audio_file, model="medium"):
    system_script = (
        f"whisper input/{audio_file} --model {model} -f all --output_dir output"
    )
    print(system_script)
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


if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=0Vjh5d5rez0"
    # file_name = "video_audio"
    # youtube_url = "https://www.youtube.com/watch?v=mjwgy3nzIlI&t=2s"
    file_name = "Cernobil2024"
    file_name_mp3 = f"{file_name}.mp3"

    print(f"Downloading audio... {youtube_url}")
    # download_audio(youtube_url)
    # transcribe_audio_whisper(file_name)

    print(f"Transcribing audio... {file_name_mp3}")
    # transcribe_audio_whisper_lib(file_name_mp3)
    # print("Transcription complete!")

    transcribe_audio2srt_fast_whisper(file_name_mp3, task="translate")

    if False:
        # print("Write to file...")
        transcription = transcribe_audio_whisper_lib(file_name_mp3)
        with open(f"output/{file_name}.txt", "w") as f:
            f.write(transcription)
