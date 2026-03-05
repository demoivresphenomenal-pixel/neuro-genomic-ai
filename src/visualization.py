"""
Visualization Module

Creates plots and visualizations for exploratory data analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class SignalVisualizer:
    """Visualizes physiological signals."""
    
    @staticmethod
    def plot_signal(data: pd.Series, title: str = "Signal", ylabel: str = "Amplitude"):
        """Plot a single time-series signal."""
        plt.figure(figsize=(12, 4))
        plt.plot(data.values, linewidth=0.8)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylabel(ylabel)
        plt.xlabel('Time')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_multiple_signals(data: pd.DataFrame, title: str = "Signals"):
        """Plot multiple signals in subplots."""
        n_signals = len(data.columns)
        fig, axes = plt.subplots(n_signals, 1, figsize=(12, 3*n_signals))
        
        if n_signals == 1:
            axes = [axes]
        
        for idx, column in enumerate(data.columns):
            axes[idx].plot(data[column].values, linewidth=0.8)
            axes[idx].set_title(column, fontweight='bold')
            axes[idx].set_ylabel('Amplitude')
            axes[idx].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.001)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_signal_distribution(data: pd.Series, title: str = "Distribution"):
        """Plot histogram and KDE of signal."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        axes[0].hist(data.values, bins=30, alpha=0.7, edgecolor='black')
        axes[0].set_title(f'{title} - Histogram', fontweight='bold')
        axes[0].set_xlabel('Value')
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        sns.kdeplot(data=data, ax=axes[1], fill=True)
        axes[1].set_title(f'{title} - Distribution', fontweight='bold')
        axes[1].set_xlabel('Value')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class AnalysisVisualizer:
    """Visualizes analysis results."""
    
    @staticmethod
    def plot_feature_importance(importance_df: pd.DataFrame, top_n: int = 15):
        """Plot feature importance."""
        top_features = importance_df.head(top_n)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_features, y='feature', x='importance', palette='viridis')
        plt.title(f'Top {top_n} Feature Importance', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_correlation_matrix(data: pd.DataFrame, figsize: tuple = (10, 8)):
        """Plot correlation heatmap."""
        plt.figure(figsize=figsize)
        correlation = data.corr()
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, cbar_kws={'label': 'Correlation'})
        plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plt.gcf()
