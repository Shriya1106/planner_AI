"""Budget prediction ML model."""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from typing import Dict, List, Optional
import joblib
import logging

logger = logging.getLogger(__name__)


class BudgetPredictor:
    """ML model for predicting budget allocation."""
    
    def __init__(self):
        """Initialize budget predictor."""
        self.model = None
        self.label_encoders = {}
        self.feature_columns = [
            "event_type",
            "city",
            "guest_count",
            "total_budget"
        ]
        self.target_categories = [
            "venue",
            "catering",
            "decoration",
            "photography",
            "entertainment",
            "transportation"
        ]
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for training/prediction.
        
        Args:
            data: Raw data DataFrame
            
        Returns:
            Processed features DataFrame
        """
        df = data.copy()
        
        # Encode categorical variables
        for col in ["event_type", "city"]:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col])
                else:
                    df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def train(self, training_data: pd.DataFrame):
        """Train budget prediction model.
        
        Args:
            training_data: Training dataset with features and targets
        """
        logger.info("Training budget prediction model")
        
        # Prepare features
        X = self.prepare_features(training_data[self.feature_columns])
        
        # Train separate models for each category
        self.model = {}
        for category in self.target_categories:
            if category in training_data.columns:
                y = training_data[category]
                
                # Use Gradient Boosting for better predictions
                model = GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=42
                )
                model.fit(X, y)
                self.model[category] = model
                
                logger.info(f"Trained model for {category}")
        
        logger.info("Budget prediction model training complete")
    
    def predict(self, event_data: Dict) -> Dict[str, float]:
        """Predict budget allocation for an event.
        
        Args:
            event_data: Event details (event_type, city, guest_count, total_budget)
            
        Returns:
            Predicted budget allocation per category
        """
        if not self.model:
            logger.warning("Model not trained, using default allocations")
            return self._default_allocation(event_data)
        
        # Prepare input features
        input_df = pd.DataFrame([event_data])
        X = self.prepare_features(input_df[self.feature_columns])
        
        # Predict for each category
        predictions = {}
        for category, model in self.model.items():
            predictions[category] = float(model.predict(X)[0])
        
        # Normalize to ensure sum equals total budget
        total_predicted = sum(predictions.values())
        if total_predicted > 0:
            scale_factor = event_data["total_budget"] / total_predicted
            predictions = {k: v * scale_factor for k, v in predictions.items()}
        
        return predictions
    
    def _default_allocation(self, event_data: Dict) -> Dict[str, float]:
        """Provide default budget allocation.
        
        Args:
            event_data: Event details
            
        Returns:
            Default budget allocation
        """
        total_budget = event_data["total_budget"]
        event_type = event_data.get("event_type", "birthday")
        
        # Default percentages by event type
        default_percentages = {
            "wedding": {
                "venue": 0.30,
                "catering": 0.25,
                "photography": 0.15,
                "decoration": 0.15,
                "entertainment": 0.10,
                "transportation": 0.05,
            },
            "corporate": {
                "venue": 0.35,
                "catering": 0.30,
                "entertainment": 0.20,
                "transportation": 0.15,
            },
            "birthday": {
                "venue": 0.25,
                "catering": 0.30,
                "entertainment": 0.20,
                "decoration": 0.15,
                "photography": 0.10,
            },
        }
        
        percentages = default_percentages.get(event_type, default_percentages["birthday"])
        return {k: v * total_budget for k, v in percentages.items()}
    
    def save_model(self, filepath: str):
        """Save trained model to disk.
        
        Args:
            filepath: Path to save model
        """
        if self.model:
            joblib.dump({
                "model": self.model,
                "label_encoders": self.label_encoders,
                "feature_columns": self.feature_columns
            }, filepath)
            logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk.
        
        Args:
            filepath: Path to load model from
        """
        data = joblib.load(filepath)
        self.model = data["model"]
        self.label_encoders = data["label_encoders"]
        self.feature_columns = data["feature_columns"]
        logger.info(f"Model loaded from {filepath}")
