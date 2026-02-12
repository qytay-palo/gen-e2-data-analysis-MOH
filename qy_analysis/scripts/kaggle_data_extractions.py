# Download specific file from Kaggle dataset
import kagglehub
import pandas as pd

# Download only the specific CSV file
path = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore",
    path="weekly-infectious-disease-bulletin-cases/weekly-infectious-disease-bulletin-cases.csv"
)

print("Downloaded file path:", path)

# Load the CSV file
df = pd.read_csv(path)
try:
    df.to_csv("weekly-infectious-disease-bulletin-cases.csv", index=False)
    print("successfully downloaded")
except Exception as e:
    print(f"Error saving CSV: {e}")

print("\nFirst 5 records:")
print(df.head())