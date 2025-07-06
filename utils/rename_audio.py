# utils/rename_audio.py
import pathlib, shutil, re

root = pathlib.Path("data/raw")
for ds in ["ravdess", "crema_d"]:
    for wav in (root/ds).rglob("*.wav"):
        # Prefix file with dataset name: ravdess_03-01-05-01-02-02-12.wav
        new = wav.with_name(f"{ds}_{wav.name.lower()}")
        wav.rename(new)
