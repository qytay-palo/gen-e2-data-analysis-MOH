"""
Quick Demo - Automated Analysis System
Demonstrates the automated LLM-driven analysis capabilities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Create sample healthcare data
print("Creating sample healthcare dataset...")

# Generate dates
start_date = datetime(2020, 1, 1)
dates = [start_date + timedelta(weeks=i) for i in range(200)]

# Generate sample data - Weekly infectious disease cases
np.random.seed(42)

data = {
    'week_ending': dates,
    'dengue_cases': np.random.poisson(50, 200) + np.sin(np.linspace(0, 8*np.pi, 200)) * 20,
    'influenza_cases': np.random.poisson(100, 200) + np.sin(np.linspace(0, 8*np.pi, 200) + 1) * 40,
    'covid_cases': np.concatenate([
        np.zeros(52),  # No COVID in 2020 Q1
        np.random.poisson(200, 52) * 5,  # Outbreak
        np.random.poisson(50, 96)  # Endemic phase
    ]),
    'hand_foot_mouth_cases': np.random.poisson(80, 200),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 200),
    'hospital_admissions': None  # Will add missing values
}

# Add some hospital admissions with missing values
admissions = (data['dengue_cases'] * 0.1 + 
              data['influenza_cases'] * 0.05 + 
              data['covid_cases'] * 0.15 + 
              np.random.normal(0, 5, 200))
admissions = np.maximum(admissions, 0)

# Introduce some missing values (10%)
missing_indices = np.random.choice(200, 20, replace=False)
admissions[missing_indices] = np.nan
data['hospital_admissions'] = admissions

# Create DataFrame
df = pd.DataFrame(data)

# Add some duplicate rows
duplicates = df.sample(5)
df = pd.concat([df, duplicates], ignore_index=True)

# Save to file
output_path = Path('data/1_raw/sample_disease_data.csv')
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✓ Sample data created: {output_path}")
print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Date range: {df['week_ending'].min()} to {df['week_ending'].max()}")
print(f"  Missing values: {df.isnull().sum().sum()}")
print(f"  Duplicates: 5 rows")

print("\n" + "="*60)
print("Now running automated analysis...")
print("="*60 + "\n")

# Import and run analyzer
import sys
sys.path.append('scripts')
from auto_analyze import AutomatedAnalyzer

analyzer = AutomatedAnalyzer()

# Run all three analysis types
for analysis_type in ['explore', 'validate', 'analyze']:
    print(f"\n{'='*60}")
    print(f"Running /{analysis_type} command")
    print(f"{'='*60}")
    
    try:
        results = analyzer.analyze_dataset(str(output_path), analysis_type)
        
        print(f"\n✓ {analysis_type.title()} complete!")
        print(f"  Timestamp: {results['timestamp']}")
        print(f"  Shape: {results['shape']['rows']} rows × {results['shape']['columns']} columns")
        
        if analysis_type == 'explore':
            print(f"  Memory: {results['memory_usage_mb']:.2f} MB")
            print(f"  Quality flags: {len(results.get('quality_flags', []))}")
        
        elif analysis_type == 'validate':
            print(f"  Duplicates: {results['duplicate_rows']} ({results['duplicate_percentage']:.1f}%)")
            print(f"  Recommendations: {len(results['recommendations'])}")
            print("\nTop recommendations:")
            for rec in results['recommendations'][:3]:
                print(f"    {rec}")
        
        elif analysis_type == 'analyze':
            corrs = results.get('correlations', {}).get('strong_correlations', [])
            outliers = results.get('outliers', {})
            print(f"  Strong correlations: {len(corrs)}")
            print(f"  Outliers detected: {len(outliers)} columns")
            
            if corrs:
                print("\n  Top correlations:")
                for corr in corrs[:3]:
                    print(f"    {corr['col1']} ↔ {corr['col2']}: r={corr['correlation']:.3f}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "="*60)
print("DEMO COMPLETE")
print("="*60)
print("\nGenerated files:")
print("  • Data: data/1_raw/sample_disease_data.csv")
print("  • Reports: reports/*.md")
print("  • Results: results/metrics/*.json")
print("\nNext steps:")
print("  1. Check the generated reports in reports/")
print("  2. Review JSON results in results/metrics/")
print("  3. Try batch analysis: python scripts/auto_analyze.py --batch data/1_raw")
print("  4. Configure schedules in config/auto_analysis.yml")
print("  5. Open notebooks/2_analysis/automated_analysis_demo.ipynb")
