
import os
import numpy as np
from torch.utils.data import Dataset
from typing import Callable, Optional, Tuple


class SimpleNumpyDataset(Dataset):
    """Simple dataset for loading .npy files from a single directory.
    
    This is useful when you have all .npy files in one folder without class subdirectories.
    
    Args:
        root_dir (str): Directory containing .npy files
        transform (callable, optional): Transform to apply to the data
        file_pattern (str, optional): Pattern to filter files (default: '*.npy')
    """
    
    def __init__(
        self,
        root_dir: str,
        transform: Optional[Callable] = None,
        file_pattern: str = '*.npy'
    ):
        self.root_dir = root_dir
        self.transform = transform
        
        # Get all .npy files
        import glob
        self.file_paths = glob.glob(os.path.join(root_dir, file_pattern))
        self.file_paths.sort()  # For consistent ordering
        
    def __len__(self) -> int:
        return len(self.file_paths)
    
    def __getitem__(self, idx: int) -> Tuple[np.ndarray, str]:
        file_path = self.file_paths[idx]
        data = np.load(file_path)
        # force to one channel for now
        data = data.reshape(1, *data.shape)
        if self.transform:
            data = self.transform(data)
            
        # Return data and filename (you can modify this as needed)
        filename = os.path.basename(file_path)
        return data, filename