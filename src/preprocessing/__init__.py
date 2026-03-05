"""
Signal Preprocessing Module

Implements bandpass filtering and artifact removal for ECG signals.
"""

import numpy as np
from scipy import signal


class ECGPreprocessor:
    """Handles ECG signal preprocessing, filtering, and normalization."""
    
    def __init__(self, sampling_rate=500, lowcut=0.5, highcut=40, filter_order=4):
        """
        Initialize ECG preprocessor.
        
        Args:
            sampling_rate (int): Sampling frequency in Hz
            lowcut (float): Low cutoff frequency in Hz (removes baseline wander)
            highcut (float): High cutoff frequency in Hz (removes noise)
            filter_order (int): Order of Butterworth filter
        """
        self.fs = sampling_rate
        self.lowcut = lowcut
        self.highcut = highcut
        self.order = filter_order
        
        # Design filter
        nyquist = self.fs / 2
        self.b, self.a = signal.butter(
            self.order,
            [lowcut / nyquist, highcut / nyquist],
            btype='band'
        )
    
    def filter_signal(self, ecg_signal):
        """
        Apply bandpass filter to ECG signal.
        
        Uses zero-phase forward-backward filtering (filtfilt) to avoid phase distortion.
        
        Args:
            ecg_signal: Input ECG signal (1D array or 2D array of channels)
            
        Returns:
            Filtered signal with same shape as input
        """
        if len(ecg_signal.shape) == 1:
            return signal.filtfilt(self.b, self.a, ecg_signal)
        else:
            # Multi-channel filtering
            filtered = np.zeros_like(ecg_signal)
            for i in range(ecg_signal.shape[1]):
                filtered[:, i] = signal.filtfilt(self.b, self.a, ecg_signal[:, i])
            return filtered
    
    def remove_baseline_wander(self, ecg_signal, window_size=None):
        """
        Remove baseline wander using median filtering.
        
        Args:
            ecg_signal: Input signal
            window_size: Window size for median filter (default: fs/50)
            
        Returns:
            Signal with baseline wander removed
        """
        if window_size is None:
            window_size = max(3, int(self.fs / 50) | 1)  # Ensure odd number
        
        baseline = signal.medfilt(ecg_signal, kernel_size=window_size)
        return ecg_signal - baseline
    
    def normalize_signal(self, ecg_signal, method='zscore'):
        """
        Normalize signal using z-score or min-max scaling.
        
        Args:
            ecg_signal: Input signal
            method: 'zscore' or 'minmax'
            
        Returns:
            Normalized signal
        """
        if method == 'zscore':
            mean = np.mean(ecg_signal, axis=0)
            std = np.std(ecg_signal, axis=0)
            return (ecg_signal - mean) / (std + 1e-8)
        elif method == 'minmax':
            minimum = np.min(ecg_signal, axis=0)
            maximum = np.max(ecg_signal, axis=0)
            return (ecg_signal - minimum) / (maximum - minimum + 1e-8)
        else:
            raise ValueError("Method must be 'zscore' or 'minmax'")
    
    def remove_powerline_noise(self, ecg_signal, notch_freq=60):
        """
        Remove powerline interference using notch filter.
        
        Args:
            ecg_signal: Input signal
            notch_freq: Powerline frequency (60 Hz US/Japan, 50 Hz Europe)
            
        Returns:
            Signal with powerline noise removed
        """
        # Design notch filter
        Q = 30  # Quality factor
        w0 = notch_freq / (self.fs / 2)
        b, a = signal.iirnotch(w0, Q)
        
        if len(ecg_signal.shape) == 1:
            return signal.filtfilt(b, a, ecg_signal)
        else:
            filtered = np.zeros_like(ecg_signal)
            for i in range(ecg_signal.shape[1]):
                filtered[:, i] = signal.filtfilt(b, a, ecg_signal[:, i])
            return filtered
    
    def get_noise_statistics(self, raw_signal, filtered_signal):
        """
        Calculate noise reduction statistics.
        
        Args:
            raw_signal: Original signal
            filtered_signal: Filtered signal
            
        Returns:
            Dictionary with noise metrics
        """
        raw_power = np.mean(raw_signal ** 2)
        filtered_power = np.mean(filtered_signal ** 2)
        noise_power = raw_power - filtered_power
        
        return {
            'raw_power': raw_power,
            'filtered_power': filtered_power,
            'noise_power': noise_power,
            'snr_improvement_db': 10 * np.log10(raw_power / (filtered_power + 1e-10))
        }
