"""Script to train budget prediction model."""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ml.budget_predictor import BudgetPredictor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


def main():
    """Train and evaluate budget prediction model."""
    print("🤖 Training Budget Prediction Model...")
    
    # Load dataset
    data_path = "data/event_planning_dataset.csv"
    if not Path(data_path).exists():
        print(f"❌ Dataset not found at {data_path}")
        print("Run: python scripts/generate_data.py first")
        return
    
    df = pd.read_csv(data_path)
    print(f"📊 Loaded dataset: {df.shape}")
    
    # Split data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    print(f"📚 Training set: {train_df.shape}")
    print(f"🧪 Test set: {test_df.shape}")
    
    # Initialize and train model
    predictor = BudgetPredictor()
    predictor.train(train_df)
    
    # Evaluate on test set
    print("\n📈 Evaluating Model Performance...")
    
    target_categories = predictor.target_categories
    results = {}
    
    for category in target_categories:
        if category in test_df.columns:
            # Prepare test data
            test_data = test_df[predictor.feature_columns + [category]].copy()
            
            # Make predictions
            predictions = []
            actuals = []
            
            for _, row in test_data.iterrows():
                event_data = {
                    'event_type': row['event_type'],
                    'city': row['city'],
                    'guest_count': row['guest_count'],
                    'total_budget': row['total_budget']
                }
                pred = predictor.predict(event_data)
                if category in pred:
                    predictions.append(pred[category])
                    actuals.append(row[category])
            
            if predictions:
                mae = mean_absolute_error(actuals, predictions)
                rmse = np.sqrt(mean_squared_error(actuals, predictions))
                r2 = r2_score(actuals, predictions)
                
                results[category] = {
                    'MAE': mae,
                    'RMSE': rmse,
                    'R²': r2
                }
                
                print(f"\n{category.upper()}:")
                print(f"  MAE:  ₹{mae:,.2f}")
                print(f"  RMSE: ₹{rmse:,.2f}")
                print(f"  R²:   {r2:.4f}")
    
    # Save model
    model_path = "models/budget_predictor.pkl"
    Path("models").mkdir(exist_ok=True)
    predictor.save_model(model_path)
    print(f"\n💾 Model saved to: {model_path}")
    
    # Test prediction
    print("\n🎯 Sample Prediction:")
    sample_event = {
        'event_type': 'wedding',
        'city': 'Bangalore',
        'guest_count': 200,
        'total_budget': 1000000
    }
    prediction = predictor.predict(sample_event)
    print(f"Event: {sample_event['event_type']} in {sample_event['city']}")
    print(f"Budget: ₹{sample_event['total_budget']:,}")
    print(f"Predicted Allocation:")
    for category, amount in prediction.items():
        percentage = (amount / sample_event['total_budget']) * 100
        print(f"  {category}: ₹{amount:,.2f} ({percentage:.1f}%)")
    
    print("\n✅ Training Complete!")


if __name__ == "__main__":
    main()
