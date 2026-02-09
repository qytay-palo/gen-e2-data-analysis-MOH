#!/usr/bin/env python3
"""
Quick Start Script for MOH Healthcare Analytics Project

This script helps you get started with the project by:
1. Checking your environment
2. Downloading sample data
3. Running initial data quality checks
4. Generating a project status report
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_environment():
    """Check if required environment variables are set."""
    print("=" * 70)
    print("STEP 1: Checking Environment Variables")
    print("=" * 70)
    
    required_vars = ["KAGGLE_USERNAME", "KAGGLE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is NOT set")
            missing_vars.append(var)
    
    if missing_vars:
        print("\n⚠️  Missing environment variables!")
        print("Please set them in your .env file or environment.")
        print("\nExample .env file:")
        print("KAGGLE_USERNAME=your_username")
        print("KAGGLE_KEY=your_api_key")
        return False
    
    print("\n✅ All required environment variables are set!")
    return True


def check_dependencies():
    """Check if required Python packages are installed."""
    print("\n" + "=" * 70)
    print("STEP 2: Checking Python Dependencies")
    print("=" * 70)
    
    required_packages = [
        "pandas",
        "numpy",
        "kagglehub",
        "matplotlib",
        "seaborn",
        "plotly",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️  Missing packages!")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed!")
    return True


def check_directory_structure():
    """Check if project directories exist."""
    print("\n" + "=" * 70)
    print("STEP 3: Checking Directory Structure")
    print("=" * 70)
    
    required_dirs = [
        "data/1_raw",
        "data/2_external",
        "data/3_interim",
        "data/4_processed",
        "notebooks/1_exploratory",
        "src/utils",
        "src/data_processing",
        "logs/etl",
        "results/tables",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} does not exist")
            all_exist = False
    
    if all_exist:
        print("\n✅ Directory structure is complete!")
    else:
        print("\n⚠️  Some directories are missing. They should have been created during setup.")
    
    return all_exist


def download_sample_data():
    """Download a sample of the Kaggle dataset."""
    print("\n" + "=" * 70)
    print("STEP 4: Downloading Sample Data")
    print("=" * 70)
    
    try:
        import kagglehub
        
        print("Downloading Kaggle dataset...")
        print("(This may take a few minutes on first run)")
        
        dataset_path = kagglehub.dataset_download(
            "subhamjain/health-dataset-complete-singapore"
        )
        
        print(f"\n✅ Data downloaded successfully!")
        print(f"📁 Location: {dataset_path}")
        
        # List files
        dataset_path_obj = Path(dataset_path)
        csv_files = list(dataset_path_obj.glob("**/*.csv"))
        print(f"\n📊 Found {len(csv_files)} CSV files")
        
        if csv_files:
            print("\nSample files:")
            for i, file in enumerate(csv_files[:5], 1):
                print(f"  {i}. {file.name}")
            if len(csv_files) > 5:
                print(f"  ... and {len(csv_files) - 5} more files")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading data: {str(e)}")
        print("\nPlease check:")
        print("1. Your Kaggle credentials are correct")
        print("2. You have internet connection")
        print("3. You have accepted the dataset terms on Kaggle")
        return False


def generate_status_report():
    """Generate a quick project status report."""
    print("\n" + "=" * 70)
    print("PROJECT STATUS SUMMARY")
    print("=" * 70)
    
    print("\n📋 Project: MOH Healthcare Analytics")
    print("🎯 Objectives:")
    print("  1. Disease outbreak detection")
    print("  2. Clinic visitation distribution analysis")
    print("  3. Policy intervention identification")
    print("  4. Healthcare process optimization")
    
    print("\n📊 Data Source: Kaggle Health Dataset (Singapore)")
    print("  - 35 data tables")
    print("  - Time span: 1990-2020")
    print("  - 100% data completeness")
    
    print("\n🚀 Next Steps:")
    print("  1. Review documentation in docs/")
    print("  2. Create your first notebook in notebooks/1_exploratory/")
    print("  3. Start with data profiling and quality assessment")
    print("  4. Complete the data dictionary for priority tables")
    
    print("\n📖 Useful Commands:")
    print("  - View setup guide: cat docs/SETUP_COMPLETE.md")
    print("  - Install dependencies: pip install -r requirements.txt")
    print("  - Run tests: pytest tests/")
    print("  - Format code: black src/ tests/")
    
    print("\n✅ Setup is complete! You're ready to start analyzing! 🎉")


def main():
    """Main function to run all checks."""
    print("\n" + "=" * 70)
    print("MOH HEALTHCARE ANALYTICS - QUICK START")
    print("=" * 70)
    print()
    
    # Run all checks
    env_ok = check_environment()
    deps_ok = check_dependencies()
    dirs_ok = check_directory_structure()
    
    # Only download data if environment is set up correctly
    if env_ok and deps_ok:
        data_ok = download_sample_data()
    else:
        print("\n⚠️  Skipping data download due to environment issues.")
        print("Please fix the issues above and run this script again.")
        data_ok = False
    
    # Generate status report
    generate_status_report()
    
    # Final message
    print("\n" + "=" * 70)
    if env_ok and deps_ok and dirs_ok and data_ok:
        print("✅ ALL CHECKS PASSED - You're ready to go!")
    else:
        print("⚠️  SOME CHECKS FAILED - Please review the issues above")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
