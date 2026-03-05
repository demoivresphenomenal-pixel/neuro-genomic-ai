"""
Signal Separation Module

Implements Independent Component Analysis (ICA) for maternal-fetal ECG separation.
"""

import numpy as np
from sklearn.decomposition import FastICA, PCA


class SignalSeparator:
    """Separates mixed signals using Independent Component Analysis."""
    
    def __init__(self, n_components=2, random_state=42):
        """
        Initialize signal separator.
        
        Args:
            n_components (int): Number of independent components to extract
            random_state (int): Random seed for reproducibility
        """
        self.n_components = n_components
        self.ica = FastICA(
            n_components=n_components,
            max_iter=500,
            random_state=random_state,
            whiten='unit-variance'
        )
        self.components_ = None
        self.mixing_matrix_ = None
    
    def fit_transform(self, mixed_signals):
        """
        Fit ICA model and return independent components.
        
        Args:
            mixed_signals: Input mixed signals (n_samples, n_channels)
            
        Returns:
            Independent components (n_samples, n_components)
        """
        self.components_ = self.ica.fit_transform(mixed_signals)
        self.mixing_matrix_ = self.ica.mixing_
        return self.components_
    
    def get_sources(self):
        """Get the extracted independent components."""
        if self.components_ is None:
            raise ValueError("Model not fitted yet. Call fit_transform first.")
        return self.components_
    
    def get_mixing_matrix(self):
        """Get the mixing matrix showing how sources combine into observations."""
        if self.mixing_matrix_ is None:
            raise ValueError("Model not fitted yet. Call fit_transform first.")
        return self.mixing_matrix_
    
    def get_unmixing_matrix(self):
        """Get the unmixing matrix (inverse of mixing matrix)."""
        if self.ica.components_ is None:
            raise ValueError("Model not fitted yet. Call fit_transform first.")
        return self.ica.components_
    
    def reconstruct_signal(self, component_index):
        """
        Reconstruct original mixed signal from a single component.
        
        Args:
            component_index (int): Index of component to use
            
        Returns:
            Reconstructed signal from single component
        """
        single_component = np.zeros_like(self.components_)
        single_component[:, component_index] = self.components_[:, component_index]
        
        # Reconstruct using inverse of unmixing matrix
        unmixing_inv = np.linalg.pinv(self.ica.components_)
        return single_component @ unmixing_inv.T
    
    def estimate_quality(self, original_mixed, reconstructed):
        """
        Estimate quality of signal separation.
        
        Args:
            original_mixed: Original mixed signal
            reconstructed: Reconstructed signal from separated components
            
        Returns:
            Quality metrics dictionary
        """
        # Normalized mean square error
        nmse = np.mean((original_mixed - reconstructed) ** 2) / np.mean(original_mixed ** 2)
        
        # Correlation (should be high for good reconstruction)
        correlation = np.corrcoef(original_mixed.flatten(), reconstructed.flatten())[0, 1]
        
        return {
            'nmse': nmse,
            'correlation': correlation,
            'reconstruction_error_percent': nmse * 100
        }


class ComponentAnalyzer:
    """Analyzes and identifies separated components."""
    
    @staticmethod
    def estimate_component_frequency(component, sampling_rate):
        """
        Estimate dominant frequency of a component using FFT.
        
        Args:
            component: Signal component
            sampling_rate: Sampling frequency in Hz
            
        Returns:
            Dominant frequency in Hz
        """
        fft = np.abs(np.fft.fft(component))
        freqs = np.fft.fftfreq(len(component), 1 / sampling_rate)
        
        # Find dominant frequency in physiological range (0.5-5 Hz for HR)
        valid_idx = (freqs > 0.5) & (freqs < 5)
        peak_idx = np.argmax(fft[valid_idx])
        
        return freqs[valid_idx][peak_idx]
    
    @staticmethod
    def classify_components(components, sampling_rate):
        """
        Classify components as maternal or fetal based on frequency.
        
        Args:
            components: All independent components
            sampling_rate: Sampling frequency in Hz
            
        Returns:
            Dictionary with classification results
        """
        classifications = {}
        frequencies = {}
        
        for i, comp in enumerate(components.T):
            freq = ComponentAnalyzer.estimate_component_frequency(comp, sampling_rate)
            frequencies[i] = freq
            
            # Maternal HR: ~60-100 bpm (1-1.67 Hz)
            # Fetal HR: ~120-160 bpm (2-2.67 Hz)
            if freq < 1.5:
                classifications[i] = 'Unknown (slow)'
            elif 1.5 <= freq < 2.0:
                classifications[i] = 'Maternal'
            elif 2.0 <= freq < 3.0:
                classifications[i] = 'Fetal'
            else:
                classifications[i] = 'Unknown (fast)'
        
        return {'classifications': classifications, 'frequencies': frequencies}
