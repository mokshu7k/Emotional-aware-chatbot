import csv
import pathlib

if __name__ == "__main__":
    # Define paths relative to the project root
    project_root = pathlib.Path(__file__).parent.parent
    balanced_dataset_dir = project_root / "data" / "processed" / "balanced_dataset"
    output_path = project_root / "data" / "processed" / "metadata_balanced.csv"

    if not balanced_dataset_dir.exists():
        print(f"Error: The directory {balanced_dataset_dir.as_posix()} does not exist.")
        exit()

    print(f"Creating metadata for balanced dataset at {balanced_dataset_dir.as_posix()}...")

    with open(output_path, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["filepath", "emotion"])

        total_files = 0
        for wav_file in balanced_dataset_dir.rglob("*.wav"):
            # Filenames are in the format: 'emotion_...wav'
            # We can get the emotion from the first part of the filename.
            try:
                # Get the filename (e.g., 'calm_ravdess_...wav')
                name = wav_file.name.lower()
                # Split by the first underscore to get the emotion
                emotion = name.split('_', 1)[0]
                
                # Check if the extracted emotion is a valid label
                valid_emotions = {"angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"}
                if emotion in valid_emotions:
                    writer.writerow([wav_file.as_posix(), emotion])
                    total_files += 1
                else:
                    print(f"Warning: Could not extract a valid emotion from filename: {name}. Skipping.")

            except Exception as e:
                print(f"Error processing file {wav_file.name}: {e}. Skipping.")

    print(f"\nMetadata created successfully at {output_path.as_posix()}")
    print(f"Total files in new metadata: {total_files}")
    print("Your model training script should now use this new file.")