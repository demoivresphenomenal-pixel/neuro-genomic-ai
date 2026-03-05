"""
Data Pipeline Module

Handles loading and initial processing of physiological, genomic, and behavioral data.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataPipeline:
    """Manages data loading and aggregation from multiple sources."""
    
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = Path(data_dir)
        self.physio_data = None
        self.genomic_data = None
        self.behavioral_data = None
    
    def load_physiological_data(self, filename: str) -> pd.DataFrame:
        """Load physiological signals data."""
        path = self.data_dir / "physio" / filename
        self.physio_data = pd.read_csv(path)
        return self.physio_data
    
    def load_genomic_data(self, filename: str) -> pd.DataFrame:
        """Load genomic expression data."""
        path = self.data_dir / "genomic" / filename
        self.genomic_data = pd.read_csv(path)
        return self.genomic_data
    
    def load_behavioral_data(self, filename: str) -> pd.DataFrame:
        """Load behavioral interaction data."""
        path = self.data_dir / "behavioral" / filename
        self.behavioral_data = pd.read_csv(path)
        return self.behavioral_data
    
    def get_dataset_summary(self) -> dict:
        """Get summary statistics of loaded datasets."""
        summary = {}
        if self.physio_data is not None:
            summary['physiological'] = {
                'shape': self.physio_data.shape,
                'columns': list(self.physio_data.columns)
            }
        if self.genomic_data is not None:
            summary['genomic'] = {
                'shape': self.genomic_data.shape,
                'columns': list(self.genomic_data.columns)
            }
        if self.behavioral_data is not None:
            summary['behavioral'] = {
                'shape': self.behavioral_data.shape,
                'columns': list(self.behavioral_data.columns)
            }
        return summary
