# utils/rename_audio.py
import pathlib, shutil, re

root = pathlib.Path("data/raw")

def clean_and_rename(file_path: pathlib.Path, dataset_prefix: str):
    current_name = file_path.name.lower()
    cleaned_name = current_name
    prefixes = ["ravdess_", "crema_d_"]

    for prefix in prefixes:
        while cleaned_name.startswith(prefix):
            cleaned_name = cleaned_name.removeprefix(prefix)

    new_name = f"{dataset_prefix}{cleaned_name}"
    new_path = file_path.with_name(new_name)

    if file_path != new_path:
        file_path.rename(new_path)
        print(f"Renamed: {file_path.name} -> {new_path.name}")
    else:
        print(f"Already correctly named: {file_path.name}")

if __name__ == "__main__":
    for ds in ["ravdess", "crema_d"]:
        prefix_to_apply = f"{ds}_"
        for wav in (root/ds).rglob("*.wav"):
            clean_and_rename(wav, prefix_to_apply)
