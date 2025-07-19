import csv, re
from pathlib import Path

def ravdess_label(fname):
    code = int(fname.split("-")[2])
    mapping = {1:"neutral",2:"calm",3:"happy",4:"sad",
               5:"angry",6:"fearful",7:"disgust",8:"surprised"}
    return mapping[code]

def crema_label(fname):
    code = fname.split("_")[-2]
    mapping = {
        "ang":"angry", "dis":"disgust", "fea":"fearful",
        "hap":"happy", "neu":"neutral", "sad":"sad"
    }
    return mapping[code]

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    out_path = project_root / "data" / "processed"
    out_path.mkdir(parents=True, exist_ok=True)
    
    metadata_file_path = out_path / "metadata.csv"
    with open(metadata_file_path, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["filepath", "emotion"])

        root = project_root / "data" / "raw"
        for wav in root.rglob("*.wav"):
            name = wav.name.lower()
            if "ravdess" in name:
                emo = ravdess_label(name)
            else:
                emo = crema_label(name)
            
            # --- CORRECTED LINE ---
            # Save the full relative path from the project root
            writer.writerow([wav.relative_to(project_root).as_posix(), emo])

    print("metadata.csv written with",
          sum(1 for _ in open(metadata_file_path)) - 1, "rows")