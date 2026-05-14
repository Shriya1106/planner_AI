"""Script to generate event planning dataset."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.data_generator import generate_event_dataset, save_dataset


def main():
    """Generate and save event planning dataset."""
    print("🎯 Generating Event Planning Dataset...")
    
    # Generate dataset
    df = generate_event_dataset(n_samples=1000, seed=42)
    
    # Save to file
    output_path = "data/event_planning_dataset.csv"
    save_dataset(df, output_path)
    
    print(f"\n✅ Dataset generated successfully!")
    print(f"📊 Shape: {df.shape}")
    print(f"💾 Saved to: {output_path}")
    print(f"\n📈 Summary Statistics:")
    print(df[['total_budget', 'guest_count']].describe())
    print(f"\n📋 Event Type Distribution:")
    print(df['event_type'].value_counts())
    print(f"\n🏙️ City Distribution:")
    print(df['city'].value_counts())


if __name__ == "__main__":
    main()
