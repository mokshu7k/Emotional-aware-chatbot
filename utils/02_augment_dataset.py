import librosa
import soundfile as sf
import os
import numpy as np
import random
import math
import pandas as pd
from collections import Counter
import shutil
import pathlib

def augment_and_save_audio(
    input_audio_path: str,
    output_dir: str,
    original_label: str,
    sr: int = 22050,
    time_stretch_factors: list = None,
    pitch_shift_steps: list = None,
    noise_amplitude_factors: list = None,
):
    try:
        y, current_sr = librosa.load(input_audio_path, sr=sr)
        base_filename = os.path.splitext(os.path.basename(input_audio_path))[0]
        
        augmented_y = y.copy()
        aug_description = []

        available_augmentations = []
        if time_stretch_factors: available_augmentations.append("time_stretch")
        if pitch_shift_steps: available_augmentations.append("pitch_shift")
        if noise_amplitude_factors: available_augmentations.append("noise_addition")

        if not available_augmentations:
            print(f"Warning: No augmentation parameters provided for {input_audio_path}. Skipping augmentation.")
            return

        num_types_to_apply = random.randint(1, len(available_augmentations))
        types_for_this_iteration = random.sample(available_augmentations, num_types_to_apply)

        if "time_stretch" in types_for_this_iteration and time_stretch_factors:
            stretch_factor = random.choice(time_stretch_factors)
            augmented_y = librosa.effects.time_stretch(augmented_y, rate=stretch_factor)
            aug_description.append(f"ts{stretch_factor:.2f}")

        if "pitch_shift" in types_for_this_iteration and pitch_shift_steps:
            pitch_step = random.choice(pitch_shift_steps)
            augmented_y = librosa.effects.pitch_shift(augmented_y, sr=current_sr, n_steps=pitch_step)
            aug_description.append(f"ps{pitch_step}")

        if "noise_addition" in types_for_this_iteration and noise_amplitude_factors:
            noise_amplitude = random.choice(noise_amplitude_factors)
            noise = np.random.randn(len(augmented_y))
            augmented_y = augmented_y + noise_amplitude * noise
            aug_description.append(f"noise{noise_amplitude:.3f}")

        aug_filename = f"{original_label}_{base_filename}_aug_{'_'.join(aug_description)}_{random.randint(1, 100000)}.wav"
        output_path = os.path.join(output_dir, aug_filename)

        while os.path.exists(output_path):
            aug_filename = f"{original_label}_{base_filename}_aug_{'_'.join(aug_description)}_{random.randint(1, 100000)}.wav"
            output_path = os.path.join(output_dir, aug_filename)

        sf.write(output_path, augmented_y, current_sr)

    except Exception as e:
        print(f"Error processing {input_audio_path}: {e}")

# --- Main script for dataset augmentation (CORRECTED) ---
if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent.parent
    processed_dir = project_root / "data" / "processed"
    metadata_path = processed_dir / "metadata.csv"
    balanced_dataset_dir = processed_dir / "balanced_dataset"
    
    os.makedirs(balanced_dataset_dir, exist_ok=True)

    if not os.path.exists(metadata_path):
        print(f"Error: metadata.csv not found at {metadata_path}. Please check your file path.")
        exit()

    metadata_df = pd.read_csv(metadata_path)
    
    current_counts = metadata_df['emotion'].value_counts()
    print("Current class distribution:")
    print(current_counts)

    target_count = max(current_counts)
    minority_emotions = [
        emotion for emotion, count in current_counts.items() 
        if count < target_count
    ]
    
    print(f"\n--- Starting Data Augmentation to balance classes to {target_count} samples ---")
    
    # --- CORRECTED COPYING LOGIC ---
    print(f"Copying and renaming all original files to '{balanced_dataset_dir.as_posix()}'...")
    files_copied_count = 0
    for _, row in metadata_df.iterrows():
        # Resolve the full path to the original file
        src_path = project_root / row['filepath']
        
        # We also need to get the final filename to add the emotion prefix
        base_filename = os.path.basename(row['filepath'])
        new_filename = f"{row['emotion']}_{base_filename}"
        
        dest_path = os.path.join(balanced_dataset_dir, new_filename)
        
        if os.path.exists(src_path) and not os.path.exists(dest_path):
            shutil.copy(src_path, dest_path)
            files_copied_count += 1
    print(f"Finished copying {files_copied_count} original files.")
    
    files_augmented_count = 0
    for emotion in minority_emotions:
        emotion_files_df = metadata_df[metadata_df['emotion'] == emotion]
        current_count = len(emotion_files_df)
        num_needed = target_count - current_count
        
        if current_count == 0:
            print(f"No files for {emotion}. Cannot augment.")
            continue

        print(f"Processing '{emotion}': original count {current_count}. Need {num_needed} new samples.")

        # The file list now contains the full paths to the source files from the metadata
        file_list = [project_root / row['filepath'] for _, row in emotion_files_df.iterrows()]
        
        aug_params = {
            "calm": {"time_stretch_factors": [0.9, 1.1], "pitch_shift_steps": [-2, 2], "noise_amplitude_factors": [0.001, 0.005]},
            "surprised": {"time_stretch_factors": [0.95, 1.05], "pitch_shift_steps": [-3, 3], "noise_amplitude_factors": [0.002, 0.008]},
            "neutral": {"time_stretch_factors": [0.98, 1.02], "pitch_shift_steps": [-1, 1], "noise_amplitude_factors": [0.0005, 0.001]},
        }
        
        for i in range(num_needed):
            file_to_augment = random.choice(file_list)
            augment_and_save_audio(
                input_audio_path=str(file_to_augment),
                output_dir=str(balanced_dataset_dir),
                original_label=emotion,
                sr=22050,
                **aug_params.get(emotion, {})
            )
            files_augmented_count += 1
    
    print(f"\n--- Augmentation Process Complete ---")
    print(f"A balanced dataset has been created at: {balanced_dataset_dir.as_posix()}")
    print(f"Total files copied: {files_copied_count}")
    print(f"Total files augmented: {files_augmented_count}")
    print("Your model training scripts should now use this new directory for data.")