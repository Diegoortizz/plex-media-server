import os

# Specify the paths to your folders
folder1_path = '/home/diego/htpc-download-box/psg_merger/posters'
folder2_path = '/home/diego/htpc-download-box/psg_merger/posters2'

# List all .webp files in each folder
def list_files(folder_path):
    return set(f for f in os.listdir(folder_path) if f.endswith('.webp'))

# Get file lists
files_folder1 = list_files(folder1_path)
files_folder2 = list_files(folder2_path)

# Find files unique to each folder
unique_to_folder1 = files_folder1 - files_folder2
unique_to_folder2 = files_folder2 - files_folder1

# Print the unique files
print("Files unique to", folder1_path + ":")
if unique_to_folder1:
    for file_name in unique_to_folder1:
        print(file_name)
else:
    print("None")

print("\nFiles unique to", folder2_path + ":")
if unique_to_folder2:
    for file_name in unique_to_folder2:
        print(file_name)
else:
    print("None")
