import os
from datetime import datetime

# Define the directory path
directory_path = "/media/downloads/complete/Presse - Le Monde/"

# List all files in the directory
files = os.listdir(directory_path)

# Filter out files that do not follow the expected naming convention
le_monde_files = [f for f in files if f.startswith("Le Monde du ") and f.endswith(".pdf")]

# Function to extract the date from the file name
def extract_date(file_name):
    date_str = file_name[len("Le Monde du "):-len(".pdf")]
    return datetime.strptime(date_str, "%d.%m.%Y")

def extract_pdf_path():
    # Find the most recent file
    if le_monde_files:
        most_recent_file = max(le_monde_files, key=lambda f: extract_date(f))
        most_recent_file_path = os.path.join(directory_path, most_recent_file)
        print(f"The most recent file is: {repr(most_recent_file_path)}")
    else:
        print("No files found in the specified directory.")
    return most_recent_file_path