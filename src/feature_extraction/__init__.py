"""
Feature Extraction Module

Extracts heart rate and HRV features from separated ECG components.
"""

import numpy as np
from scipy.signal import find_peaks


class HRVExtractor:
    """Extracts heart rate variability features from ECG signals."""
    
    def __init__(self, sampling_rate=500):
        """
        Initialize HRV extractor.
        
        Args:
            sampling_rate (int): Sampling frequency in Hz
        """
        self.fs = sampling_rate
    
    def detect_r_peaks(self, ecg_signal, threshold_multiplier=2.0):
        """
        Detect R-peaks in ECG signal.
        
        Args:
            ecg_signal: Input ECG signal
            threshold_multiplier: Multiplier for adaptive threshold
            
        Returns:
            Array of R-peak indices
        """
        signal_abs = np.abs(ecg_signal)
        threshold = np.mean(signal_abs) + threshold_multiplier * np.std(signal_abs)
        
        # Minimum distance between peaks (bpm = 200 ~= 0.4 s minimum)
        min_distance = int(self.fs * 0.4)
        
        peaks, _ = find_peaks(signal_abs, height=threshold, distance=min_distance)
        return peaks
    
    def extract_features(self, ecg_signal):
        """
        Extract HRV features from ECG signal.
        
        Args:
            ecg_signal: Input ECG signal
            
        Returns:
            Dictionary with HRV features
        """
        # Detect R-peaks
        peaks = self.detect_r_peaks(ecg_signal)
        
        if len(peaks) < 2:
            return self._get_empty_features()
        
        # Calculate inter-beat intervals (RR intervals in milliseconds)
        rr_intervals = np.diff(peaks) / self.fs * 1000
        
        # Time-domain features
        heart_rate = 60 / (np.mean(rr_intervals) / 1000)
        hr_std = np.std(60 / (rr_intervals / 1000))
        
        # RR interval statistics
        rr_mean = np.mean(rr_intervals)
        rr_std = np.std(rr_intervals)
        
        # Advanced HRV metrics
        rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2))
        pnn50 = 100 * np.sum(np.abs(np.diff(rr_intervals)) > 50) / len(rr_intervals)
        
        # Frequency-domain features would be added here
        
        return {
            'num_beats': len(peaks),
            'heart_rate_mean': heart_rate,
            'heart_rate_std': hr_std,
            'rr_interval_mean': rr_mean,
            'rr_interval_std': rr_std,
            'rmssd': rmssd,  # Root mean square of successive differences
            'pnn50': pnn50,   # Percent of RR intervals differing > 50 ms
            'r_peaks': peaks,
            'rr_intervals': rr_intervals
        }
    
    @staticmethod
    def _get_empty_features():
        """Return features with NaN values when no beats are detected."""
        return {
            'num_beats': 0,
            'heart_rate_mean': np.nan,
            'heart_rate_std': np.nan,
            'rr_interval_mean': np.nan,
            'rr_interval_std': np.nan,
            'rmssd': np.nan,
            'pnn50': np.nan,
            'r_peaks': np.array([]),
            'rr_intervals': np.array([])
        }
    
    def extract_batch_features(self, signals_dict):
        """
        Extract features from multiple signals.
        
        Args:
            signals_dict: Dictionary with signal names as keys and signals as values
            
        Returns:
            Dictionary of feature dictionaries for each signal
        """
        results = {}
        for name, signal in signals_dict.items():
            results[name] = self.extract_features(signal)
        return results
