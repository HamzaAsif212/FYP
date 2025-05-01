import pandas as pd
import os

# Define the folder containing the CSV files
folder_path = r'C:\Users\asifh\Downloads\agro-scan\agro-scan\hardware'  # Use raw string to avoid escape issues

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Check if there are any CSV files
if not csv_files:
    print("No CSV files found in the specified folder.")
    exit()

# Read all CSV files into a dictionary of DataFrames
dataframes = {}
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    dataframes[file] = pd.read_csv(file_path)

# Combine all DataFrames column-wise (horizontally)
merged_df = pd.concat(dataframes.values(), axis=1)

# Save the merged DataFrame to a new CSV file
output_file = 'merged_output.csv'
merged_df.to_csv(output_file, index=False)

print(f"All CSV files have been merged into {output_file}.")