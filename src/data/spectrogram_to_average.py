import os
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

ROOT = Path(__file__).parents[2]

# Directory containing 2D spectrograms (assumed to be .npy files)
DATA_DIR = ROOT / "data_collection" / "spectrograms" / "data" / "arrays"
PIPELINE_DIR = ROOT / "data_collection" / "spectrograms" / "models" / "pipelines"

SPECTROGRAM_DIR = DATA_DIR / "train_sample"

# Output directory for 1D averaged arrays
OUTPUT_DIR = DATA_DIR / "train_sample_averaged"

# Collect all averaged arrays for fitting the scaler
averaged_arrays = []
file_names = []

for fname in os.listdir(SPECTROGRAM_DIR):
    if fname.endswith('.npy'):
        path = os.path.join(SPECTROGRAM_DIR, fname)
        spectrogram = np.load(path)  # shape: (height, width)
        averaged = np.mean(spectrogram, axis=1)
        averaged_arrays.append(averaged)
        file_names.append(fname)

# Stack to shape (n_samples, n_features)
X = np.stack(averaged_arrays)

# Fit scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler pipeline
scaler_path = PIPELINE_DIR / "scaler.joblib"
joblib.dump(scaler, scaler_path)

# Save the normalised arrays
for i, fname in enumerate(file_names):
    out_path = OUTPUT_DIR / fname
    np.save(out_path, X_scaled[i])
