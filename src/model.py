"""
Machine Learning Model Module

Implements classification and regression models for cognitive state prediction.
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error
import numpy as np
import pandas as pd


class CognitiveStateClassifier:
    """Classifies user cognitive states (focused, distracted, overloaded)."""
    
    def __init__(self, model_type: str = 'rf'):
        """
        Initialize classifier.
        
        Args:
            model_type: 'rf' (Random Forest) or 'gb' (Gradient Boosting)
        """
        if model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'gb':
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError("Model type must be 'rf' or 'gb'")
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train the classifier."""
        self.model.fit(X_train, y_train)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        return self.model.predict(X)
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Evaluate model performance."""
        predictions = self.predict(X_test)
        return {
            'accuracy': accuracy_score(y_test, predictions),
            'f1_score': f1_score(y_test, predictions, average='weighted'),
        }
    
    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        """Get feature importance scores."""
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance


class AdaptivityPredictor:
    """Predicts optimal interface adaptations based on user state."""
    
    def __init__(self):
        self.classifier = CognitiveStateClassifier(model_type='rf')
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Fit the adaptation predictor."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.classifier.train(X_train, y_train)
        return self.classifier.evaluate(X_test, y_test)
    
    def suggest_adaptation(self, user_state: dict) -> str:
        """Suggest interface adaptation based on cognitive state."""
        # Placeholder for adaptation logic
        if user_state.get('cognitive_load', 0) > 0.7:
            return 'REDUCE_COMPLEXITY'
        elif user_state.get('engagement', 0) < 0.3:
            return 'INCREASE_INTERACTIVITY'
        else:
            return 'MAINTAIN_CURRENT'
