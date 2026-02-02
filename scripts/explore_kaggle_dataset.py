"""
Kaggle Dataset Explorer
Explores the Singapore Health Dataset and generates comprehensive documentation
"""

import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import json
import os
from pathlib import Path

def explore_dataset():
    """Explore and document the Kaggle Singapore Health Dataset"""
    
    print("=" * 80)
    print("KAGGLE DATASET EXPLORATION: Singapore Health Dataset")
    print("=" * 80)
    
    dataset_name = "subhamjain/health-dataset-complete-singapore"
    
    try:
        # Download the dataset to see all files
        print("\n1. Downloading dataset to inspect files...")
        dataset_path = kagglehub.dataset_download(dataset_name)
        print(f"   Dataset downloaded to: {dataset_path}")
        
        # List all files in the dataset
        print("\n2. Files in dataset:")
        all_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, dataset_path)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                all_files.append({
                    'filename': file,
                    'relative_path': rel_path,
                    'full_path': file_path,
                    'size_mb': round(file_size, 2)
                })
                print(f"   - {rel_path} ({file_size:.2f} MB)")
        
        # Explore each file
        print("\n3. Analyzing each file...")
        dataset_info = {
            'dataset_name': dataset_name,
            'dataset_path': dataset_path,
            'total_files': len(all_files),
            'files': []
        }
        
        for file_info in all_files:
            print(f"\n   Analyzing: {file_info['filename']}")
            print(f"   " + "-" * 60)
            
            file_data = {
                'filename': file_info['filename'],
                'relative_path': file_info['relative_path'],
                'size_mb': file_info['size_mb'],
                'file_type': None,
                'error': None
            }
            
            try:
                # Try to read the file based on extension
                file_path = file_info['full_path']
                file_ext = os.path.splitext(file_info['filename'])[1].lower()
                
                df = None
                if file_ext == '.csv':
                    df = pd.read_csv(file_path)
                    file_data['file_type'] = 'CSV'
                elif file_ext in ['.xlsx', '.xls']:
                    df = pd.read_excel(file_path)
                    file_data['file_type'] = 'Excel'
                elif file_ext == '.json':
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                    print(f"   Type: JSON")
                    print(f"   Structure: {type(json_data)}")
                    file_data['file_type'] = 'JSON'
                    file_data['structure'] = str(type(json_data))
                    continue
                else:
                    print(f"   Type: {file_ext} (unsupported for analysis)")
                    file_data['file_type'] = file_ext
                    continue
                
                if df is not None:
                    # Get basic info
                    rows, cols = df.shape
                    print(f"   Type: {file_data['file_type']}")
                    print(f"   Rows: {rows:,}")
                    print(f"   Columns: {cols}")
                    
                    file_data['rows'] = rows
                    file_data['columns'] = cols
                    file_data['column_names'] = df.columns.tolist()
                    
                    # Column details
                    print(f"\n   Column Details:")
                    column_details = []
                    for col in df.columns:
                        col_info = {
                            'name': col,
                            'dtype': str(df[col].dtype),
                            'non_null_count': int(df[col].notna().sum()),
                            'null_count': int(df[col].isna().sum()),
                            'null_percentage': round(df[col].isna().sum() / len(df) * 100, 2),
                            'unique_count': int(df[col].nunique()),
                            'sample_values': []
                        }
                        
                        # Get sample values (non-null)
                        sample = df[col].dropna().head(5).tolist()
                        col_info['sample_values'] = [str(v) for v in sample]
                        
                        # Get value counts for categorical-like columns
                        if col_info['unique_count'] <= 20:
                            value_counts = df[col].value_counts().head(10).to_dict()
                            col_info['value_distribution'] = {str(k): int(v) for k, v in value_counts.items()}
                        
                        column_details.append(col_info)
                        
                        print(f"      {col}:")
                        print(f"         Type: {col_info['dtype']}")
                        print(f"         Non-Null: {col_info['non_null_count']:,} ({100-col_info['null_percentage']:.1f}%)")
                        print(f"         Null: {col_info['null_count']:,} ({col_info['null_percentage']:.1f}%)")
                        print(f"         Unique Values: {col_info['unique_count']:,}")
                        if col_info['sample_values']:
                            print(f"         Sample: {', '.join(col_info['sample_values'][:3])}")
                    
                    file_data['column_details'] = column_details
                    
                    # Memory usage
                    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
                    file_data['memory_usage_mb'] = round(memory_mb, 2)
                    print(f"\n   Memory Usage: {memory_mb:.2f} MB")
                    
                    # Data quality summary
                    total_cells = rows * cols
                    null_cells = df.isna().sum().sum()
                    completeness = (1 - null_cells / total_cells) * 100
                    file_data['data_quality'] = {
                        'total_cells': total_cells,
                        'null_cells': int(null_cells),
                        'completeness_percentage': round(completeness, 2)
                    }
                    print(f"   Data Completeness: {completeness:.2f}%")
                    
            except Exception as e:
                print(f"   ERROR: {str(e)}")
                file_data['error'] = str(e)
            
            dataset_info['files'].append(file_data)
        
        # Save exploration results
        print("\n" + "=" * 80)
        print("4. Saving exploration results...")
        
        output_file = '/Users/qytay/Documents/GitHub/gen-e2-data-analysis-MOH/data/dataset_exploration.json'
        with open(output_file, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        print(f"   Saved to: {output_file}")
        
        print("\n" + "=" * 80)
        print("EXPLORATION COMPLETE")
        print("=" * 80)
        
        return dataset_info
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    explore_dataset()
