#!/usr/bin/env python3
"""Music Analysis Visualization Generator.

This script finds all music files in a specified directory and generates
comprehensive music analysis visualizations for each file, including:

1. Mel-Spectrogram (perceptually motivated frequency analysis)
2. Chromagram (pitch class/harmony analysis)
3. MFCC (timbral characteristics)
4. Constant-Q Transform (musical note-based frequency analysis)
5. Tempogram (rhythm and tempo analysis)

Each visualization uses the middle 2 minutes of each song for consistent analysis.
Songs shorter than 2 minutes are automatically skipped.

Requirements:
    pip install librosa matplotlib numpy soundfile typer tqdm
"""

import os
import sys
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import random
import typer
from tqdm import tqdm

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Supported audio file extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"}

app = typer.Typer(help="Generate comprehensive music analysis visualizations.")


def extract_middle_segment(
    y: np.ndarray, sr: int, duration: int = 120
) -> Optional[np.ndarray]:
    """Extract the middle segment of an audio file.

    Args:
        y: Audio time series
        sr: Sample rate
        duration: Duration in seconds to extract

    Returns:
        Middle segment of audio, or None if too short
    """
    total_duration = len(y) / sr

    if total_duration < duration:
        return None

    # Calculate start and end samples for middle segment
    start_time = (total_duration - duration) / 2
    start_sample = int(start_time * sr)
    end_sample = start_sample + int(duration * sr)

    return y[start_sample:end_sample]


def create_music_analysis_plots(
    audio_file: Path,
    output_dir: Path,
    figsize: Tuple[int, int] = (15, 12),
    sr: int = 22050,
) -> bool:
    """Create and save multiple music analysis visualizations for an audio file.

    Args:
        audio_file: Path to the audio file
        output_dir: Directory to save the visualization images
        figsize: Figure size for the plot
        sr: Sample rate for audio loading

    Returns:
        True if successful, False if failed
    """
    try:
        # Load audio file
        y, sr = librosa.load(str(audio_file), sr=sr)

        # Extract middle 2 minutes
        y_segment = extract_middle_segment(y, sr, duration=120)
        if y_segment is None:
            return False

        # Create figure with subplots
        fig, axes = plt.subplots(5, 1, figsize=figsize)
        fig.suptitle(
            f"Music Analysis: {audio_file.stem}", fontsize=16, fontweight="bold"
        )

        # 1. Mel-Spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y_segment, sr=sr, n_mels=128)
        mel_spec_db = librosa.amplitude_to_db(mel_spec, ref=np.max)
        librosa.display.specshow(
            mel_spec_db, sr=sr, x_axis="time", y_axis="mel", ax=axes[0]
        )
        axes[0].set_title("Mel-Spectrogram")
        axes[0].set_ylabel("Mel Frequency")

        # 2. Chromagram
        chroma = librosa.feature.chroma_stft(y=y_segment, sr=sr)
        librosa.display.specshow(
            chroma, sr=sr, x_axis="time", y_axis="chroma", ax=axes[1]
        )
        axes[1].set_title("Chromagram")
        axes[1].set_ylabel("Pitch Class")

        # 3. MFCC
        mfccs = librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=13)
        librosa.display.specshow(mfccs, sr=sr, x_axis="time", ax=axes[2])
        axes[2].set_title("MFCC")
        axes[2].set_ylabel("MFCC Coefficient")

        # 4. Constant-Q Transform Spectrogram
        C = np.abs(librosa.cqt(y_segment, sr=sr))
        C_db = librosa.amplitude_to_db(C, ref=np.max)
        librosa.display.specshow(
            C_db, sr=sr, x_axis="time", y_axis="cqt_note", ax=axes[3]
        )
        axes[3].set_title("Constant-Q Transform")
        axes[3].set_ylabel("Note")

        # 5. Tempogram
        onset_envelope = librosa.onset.onset_strength(y=y_segment, sr=sr)
        tempogram = librosa.feature.tempogram(onset_envelope=onset_envelope, sr=sr)
        librosa.display.specshow(
            tempogram, sr=sr, x_axis="time", y_axis="tempo", ax=axes[4]
        )
        axes[4].set_title("Tempogram")
        axes[4].set_ylabel("BPM")
        axes[4].set_xlabel("Time (s)")

        # Adjust layout
        plt.tight_layout()

        # Save the combined analysis plot
        output_file = output_dir / f"{audio_file.stem}_music_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()  # Close the figure to free memory

        return True

    except Exception as e:
        return False


def find_audio_files(directory: Path) -> List[Path]:
    """Find all audio files in the given directory.

    Args:
        directory: Directory to search for audio files

    Returns:
        List of Path objects for audio files found
    """
    audio_files = []

    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(file_path)

    return sorted(audio_files)


@app.command()
def main(
    input_dir: str = typer.Argument(
        ".", help="Input directory containing music files"
    ),
    output_dir: str = typer.Argument(
        "music_analysis", help="Output directory for music analysis images"
    ),
    figsize_width: int = typer.Option(
        15, "--figsize-width", help="Figure width for music analysis plots"
    ),
    figsize_height: int = typer.Option(
        12, "--figsize-height", help="Figure height for music analysis plots"
    ),
    sample_rate: int = typer.Option(
        22050, "--sample-rate", help="Sample rate for audio processing"
    ),
    random_sample: Optional[int] = typer.Option(
        None,
        "--random-sample",
        help="Take a random sample of N songs instead of processing all files",
    ),
    seed: Optional[int] = typer.Option(
        None, "--seed", help="Random seed for reproducible sampling"
    ),
) -> None:
    """Generate comprehensive music analysis visualizations for all music files in a directory.

    Args:
        input_dir: Input directory containing music files
        output_dir: Output directory for music analysis images
        figsize_width: Figure width for music analysis plots
        figsize_height: Figure height for music analysis plots
        sample_rate: Sample rate for audio processing
        random_sample: Take a random sample of N songs instead of processing all files
        seed: Random seed for reproducible sampling
    """
    # Convert to Path objects
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Validate input directory
    if not input_path.exists():
        print(f"Error: Input directory '{input_path}' does not exist.")
        raise typer.Exit(1)

    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.")
        raise typer.Exit(1)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_path.absolute()}")

    # Find audio files
    print(f"Searching for audio files in: {input_path.absolute()}")
    audio_files = find_audio_files(input_path)

    if not audio_files:
        print("No audio files found with supported extensions:")
        print(f"Supported formats: {', '.join(sorted(AUDIO_EXTENSIONS))}")
        raise typer.Exit(0)

    print(f"Found {len(audio_files)} audio file(s)")

    # Apply random sampling if requested
    if random_sample:
        if seed is not None:
            random.seed(seed)
            print(f"Using random seed: {seed}")

        if random_sample >= len(audio_files):
            print(
                f"Random sample size ({random_sample}) >= total files ({len(audio_files)}), processing all files"
            )
        else:
            audio_files = random.sample(audio_files, random_sample)
            print(f"Randomly selected {len(audio_files)} files for processing")

    print("-" * 50)

    # Process each audio file with progress bar
    successful = 0
    failed = 0
    skipped = 0

    progress_bar = tqdm(
        audio_files,
        desc="Processing audio files",
        unit="file",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
    )

    for audio_file in progress_bar:
        progress_bar.set_postfix_str(f"Processing: {audio_file.name}")
        
        result = create_music_analysis_plots(
            audio_file,
            output_path,
            figsize=(figsize_width, figsize_height),
            sr=sample_rate,
        )
        
        if result is True:
            successful += 1
            progress_bar.set_postfix_str(f"✓ Completed: {audio_file.name}")
        elif result is False:
            # Check if file was skipped (too short) or failed
            try:
                y, _ = librosa.load(str(audio_file), sr=sample_rate)
                if len(y) / sample_rate < 120:
                    skipped += 1
                    progress_bar.set_postfix_str(f"⚠ Skipped (too short): {audio_file.name}")
                else:
                    failed += 1
                    progress_bar.set_postfix_str(f"✗ Failed: {audio_file.name}")
            except:
                failed += 1
                progress_bar.set_postfix_str(f"✗ Failed: {audio_file.name}")

    progress_bar.close()

    # Summary
    print("-" * 50)
    print(f"Processing complete!")
    print(f"Successful: {successful}")
    print(f"Skipped (too short): {skipped}")
    print(f"Failed: {failed}")
    print(f"Music analysis plots saved to: {output_path.absolute()}")


if __name__ == "__main__":
    app()
