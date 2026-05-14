"""Generate synthetic event planning dataset."""

import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def generate_event_dataset(n_samples: int = 1000, seed: Optional[int] = 42) -> pd.DataFrame:
    """Generate synthetic event planning dataset.
    
    Args:
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with event planning data
    """
    if seed:
        np.random.seed(seed)
    
    logger.info(f"Generating {n_samples} event samples")
    
    # Event types and their characteristics
    event_types = ['wedding', 'corporate', 'birthday', 'anniversary', 'conference', 'party']
    cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad']
    
    # Budget ranges by event type (in INR)
    budget_ranges = {
        'wedding': (500000, 5000000),
        'corporate': (200000, 3000000),
        'birthday': (50000, 500000),
        'anniversary': (100000, 1000000),
        'conference': (500000, 5000000),
        'party': (50000, 300000)
    }
    
    # Guest count ranges by event type
    guest_ranges = {
        'wedding': (100, 1000),
        'corporate': (50, 500),
        'birthday': (20, 200),
        'anniversary': (30, 150),
        'conference': (100, 1000),
        'party': (30, 200)
    }
    
    # Budget allocation percentages by event type
    allocations = {
        'wedding': {
            'venue': 0.30,
            'catering': 0.25,
            'photography': 0.15,
            'decoration': 0.15,
            'entertainment': 0.10,
            'transportation': 0.05
        },
        'corporate': {
            'venue': 0.35,
            'catering': 0.30,
            'entertainment': 0.15,
            'transportation': 0.10,
            'accommodation': 0.10
        },
        'birthday': {
            'venue': 0.25,
            'catering': 0.30,
            'entertainment': 0.20,
            'decoration': 0.15,
            'photography': 0.10
        },
        'anniversary': {
            'venue': 0.30,
            'catering': 0.25,
            'decoration': 0.20,
            'photography': 0.15,
            'entertainment': 0.10
        },
        'conference': {
            'venue': 0.40,
            'catering': 0.25,
            'entertainment': 0.15,
            'accommodation': 0.15,
            'transportation': 0.05
        },
        'party': {
            'venue': 0.25,
            'catering': 0.30,
            'entertainment': 0.25,
            'decoration': 0.15,
            'photography': 0.05
        }
    }
    
    # Generate data
    data = []
    for _ in range(n_samples):
        event_type = np.random.choice(event_types)
        city = np.random.choice(cities)
        
        # Generate budget with some variation
        budget_min, budget_max = budget_ranges[event_type]
        total_budget = np.random.randint(budget_min, budget_max)
        
        # Generate guest count
        guest_min, guest_max = guest_ranges[event_type]
        guest_count = np.random.randint(guest_min, guest_max)
        
        # Calculate budget breakdown
        allocation = allocations[event_type]
        row = {
            'event_type': event_type,
            'city': city,
            'guest_count': guest_count,
            'total_budget': total_budget
        }
        
        # Add category allocations with small random variations
        for category, percentage in allocation.items():
            # Add ±5% random variation
            variation = np.random.uniform(-0.05, 0.05)
            actual_percentage = max(0.05, min(0.50, percentage + variation))
            row[category] = total_budget * actual_percentage
        
        # Normalize to ensure sum equals total budget
        category_sum = sum(row[cat] for cat in allocation.keys())
        if category_sum > 0:
            scale_factor = total_budget / category_sum
            for category in allocation.keys():
                row[category] = row[category] * scale_factor
        
        data.append(row)
    
    df = pd.DataFrame(data)
    logger.info(f"Generated dataset with shape: {df.shape}")
    
    return df


def save_dataset(df: pd.DataFrame, filepath: str):
    """Save dataset to CSV file.
    
    Args:
        df: DataFrame to save
        filepath: Path to save file
    """
    df.to_csv(filepath, index=False)
    logger.info(f"Dataset saved to {filepath}")


if __name__ == "__main__":
    # Generate and save dataset
    df = generate_event_dataset(n_samples=1000)
    save_dataset(df, "data/event_planning_dataset.csv")
    print(f"Dataset generated: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataset statistics:")
    print(df.describe())
