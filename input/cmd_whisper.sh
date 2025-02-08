insanely-fast-whisper --file-name /Users/orhancavus/LocalDocuments/BG_Politics/BG_Revival_Process.wav --model openai/whisper-large-v3 --task transcribe --transcript-path /Users/orhancavus/LocalDocuments/BG_Politics/ --device mps

venv/bin/python transcribe_youtube.py --youtube_url 'https://youtu.be/NkWV4Q9z_-E\?si\=38KfEUEUcQG5cvuX' --file_name ujas_naretchen_vp --method fast_whisper --task transcribe
venv/bin/python transcribe_youtube.py --youtube_url 'https://www.youtube.com/watch?v=PFIzUTelahs' --file_name kaka_zapotshva_vp_bg --method fast_whisper --task transcribe
venv/bin/python transcribe_youtube.py --youtube_url 'https://www.youtube.com/watch?v=gU1LYG6TLUQ' --file_name imeto_tvoeto_ime_radyo_teatir_bg --method fast_whisper --task transcribe
venv/bin/python transcribe_youtube.py --youtube_url 'https://youtu.be/VgIX5FoNVqU\?si\=8xDzh_FjtXOexxiv' --file_name ikonomika_na_vp_bg --method fast_whisper --task transcribe
venv/bin/python transcribe_youtube.py --youtube_url 'https://www.youtube.com/watch\?v\=siR4vfMaaHQ\&t\=1s' --file_name sledi_na_terora_vp_bg --method fast_whisper --task transcribe