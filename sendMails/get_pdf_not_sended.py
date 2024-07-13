import os
from datetime import datetime

# Define the directory path
directory_path = "/media/downloads/complete/Presse - Le Monde/"
record_file_path = "/home/diego/htpc-download-box/sendMails/processed_files.txt"

# List all files in the directory
files = os.listdir(directory_path)

# Filter out files that do not follow the expected naming convention
le_monde_files = [f for f in files if f.startswith("Le Monde du ") and f.endswith(".pdf")]

# Function to extract the date from the file name
def extract_date(file_name):
    date_str = file_name[len("Le Monde du "):-len(".pdf")]
    return datetime.strptime(date_str, "%d.%m.%Y")

def read_processed_files():
    """Read the list of processed files from the text file."""
    if os.path.exists(record_file_path):
        with open(record_file_path, 'r') as file:
            return file.read().splitlines()
    return []

def write_processed_files(processed_files):
    """Write the list of processed files to the text file."""
    with open(record_file_path, 'w') as file:
        for file_name in processed_files:
            file.write(file_name + '\n')

def extract_pdf_paths():
    # Read the list of already processed files
    processed_files = read_processed_files()

    # Find files that are not yet processed
    new_files = [f for f in le_monde_files if f not in processed_files]

    # Update the list of processed files
    all_processed_files = processed_files + new_files
    
    write_processed_files(all_processed_files)

    # Return the paths of the new files
    new_file_paths = [os.path.join(directory_path, f) for f in new_files]

    # if new_file_paths:
    #     print(f"New files found: {new_file_paths}")
    # else:
    #     print("No new files found in the specified directory.")

    return new_file_paths

# # Execute the function
# new_file_paths = extract_pdf_paths()