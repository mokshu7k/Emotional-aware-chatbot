# utils/build_metadata.py
import csv, re
from pathlib import Path

def ravdess_label(fname):
    # RAVDESS file names encode emotion in the 3rd group: 03-01-**05**-...
    code = int(fname.split("-")[2])
    mapping = {1:"neutral",2:"calm",3:"happy",4:"sad",
               5:"angry",6:"fearful",7:"disgust",8:"surprised"}
    return mapping[code]

def crema_label(fname):
    # CREMA-D file names: 1001_DFA_ANG_XXX.wav
    code = fname.split("_")[-2]
    mapping = {
        "ang":"angry", "dis":"disgust", "fea":"fearful",
        "hap":"happy", "neu":"neutral", "sad":"sad"
    }
    return mapping[code]

out_path = Path("data/processed")
out_path.mkdir(parents=True, exist_ok=True)   # make sure folder exists

with open(out_path / "metadata.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["filepath", "emotion"])

    root = Path("data/raw")
    for wav in root.rglob("*.wav"):
        name = wav.name.lower()
        if "ravdess" in name:
            emo = ravdess_label(name)
        else:                                 # assumes only ravdess & crema
            emo = crema_label(name)
        writer.writerow([wav.as_posix(), emo])

print("metadata.csv written with",
      sum(1 for _ in open(out_path / "metadata.csv")) - 1, "rows")
