import os

def find_files_with_one_link(root_dir):
    files_with_one_link = []
    
    # Walk through the directory and its subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            # Get file status
            try:
                stat_info = os.stat(file_path)
                # Check if the file has exactly 1 hard link
                if stat_info.st_nlink == 1:
                    files_with_one_link.append(file_path)
            except FileNotFoundError:
                # Skip if file is not found (handle any symbolic link issues, etc.)
                continue
    
    return files_with_one_link


def find_file_in_possible_paths(file_path, base_paths):
    for base_path in base_paths:
        # Construct the full path by appending the relative file path to the base path
        potential_path = os.path.join(base_path, file_path)
        
        # Check if the file exists at this location
        if os.path.exists(potential_path):
            return potential_path
    return None


def compare_files_across_drives(root_directory, possible_base_paths):
    # Collect files with 1 link from the source directory
    files = find_files_with_one_link(root_directory)
    
    for file in files:
        # Extract the relative path from the source file (part after '/complete/tv/')
        relative_path = os.path.relpath(file, root_directory)
        
        # Find the file in the possible base paths
        found_path = find_file_in_possible_paths(relative_path, possible_base_paths)
        
        # Print the comparison
        print(file)
        if found_path:
            print(f"=>\n{found_path}")
        else:
            print("=>\nNOT FOUND")
        print("---------------------------")


# Example usage
root_directory = "/mnt/das8TB/complete/tv"

# Possible base paths where the file might exist
possible_base_paths = [
    "/mnt/sdc1/complete/tv",
    "/mnt/das12TB/complete/tv"
]

# Compare the files across drives
compare_files_across_drives(root_directory, possible_base_paths)
