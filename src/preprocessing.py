"""
Preprocessing Module

Handles data cleaning, normalization, and feature engineering.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class SignalPreprocessor:
    """Preprocesses physiological signals."""
    
    @staticmethod
    def remove_artifacts(data: pd.Series, threshold: float = 3.0) -> pd.Series:
        """Remove outliers using z-score method."""
        z_scores = np.abs((data - data.mean()) / data.std())
        return data[z_scores < threshold]
    
    @staticmethod
    def normalize_signal(data: pd.Series, method: str = 'zscore') -> pd.Series:
        """Normalize signal using z-score or min-max scaling."""
        if method == 'zscore':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Method must be 'zscore' or 'minmax'")
        
        return pd.Series(
            scaler.fit_transform(data.values.reshape(-1, 1)).flatten(),
            index=data.index
        )
    
    @staticmethod
    def compute_rolling_features(data: pd.Series, window: int = 5) -> pd.DataFrame:
        """Compute rolling statistics for time-series features."""
        features = pd.DataFrame(index=data.index)
        features['rolling_mean'] = data.rolling(window=window).mean()
        features['rolling_std'] = data.rolling(window=window).std()
        features['rolling_min'] = data.rolling(window=window).min()
        features['rolling_max'] = data.rolling(window=window).max()
        
        return features.dropna()


class DataCleaner:
    """General data cleaning utilities."""
    
    @staticmethod
    def handle_missing_values(data: pd.DataFrame, method: str = 'ffill') -> pd.DataFrame:
        """Handle missing values using forward fill or interpolation."""
        if method == 'ffill':
            return data.fillna(method='ffill').fillna(method='bfill')
        elif method == 'interpolate':
            return data.interpolate(method='linear')
        else:
            raise ValueError("Method must be 'ffill' or 'interpolate'")
    
    @staticmethod
    def align_datasets(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple:
        """Align two datasets by their indices."""
        common_index = df1.index.intersection(df2.index)
        return df1.loc[common_index], df2.loc[common_index]
