import os
import shutil
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def create_hardlinks(src_dir, dest_dir):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over directories in the source directory
    for root, dirs, files in os.walk(src_dir):
        # Get the relative path of the current directory
        relative_root = os.path.relpath(root, src_dir)
        # Skip the root directory itself
        if relative_root == '.':
            continue

        # Create the corresponding target directory
        dest_folder = os.path.join(dest_dir, relative_root)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Check the number of files in the current directory
        num_files = len(files)

        if num_files == 1:
            # Case 1: Only one file, create a hardlink directly in the target folder
            src_file = os.path.join(root, files[0])
            dest_file = os.path.join(dest_folder, files[0])

            # Check if the hardlink already exists
            if os.path.exists(dest_file):
                print(f"{timestamp()} - Hardlink already exists: {os.path.relpath(dest_file, dest_dir)}")
                continue

            # Create a hardlink
            os.link(src_file, dest_file)
            print(f"{timestamp()} - Created hardlink: {os.path.relpath(dest_file, dest_dir)}")

        elif num_files == 2:
            # Case 2: Two files, create subfolders "1" and "2" based on filename contents
            for file in files:
                src_file = os.path.join(root, file)
                
                # Determine target subfolder based on filename
                if '1' in file:
                    subfolder = os.path.join(dest_folder, '1')
                elif '2' in file:
                    subfolder = os.path.join(dest_folder, '2')
                else:
                    print(f"{timestamp()} - Skipping file: {file} (does not contain '1' or '2')")
                    continue
                
                # Create the subfolder if it does not exist
                if not os.path.exists(subfolder):
                    os.makedirs(subfolder)
                
                dest_file = os.path.join(subfolder, file)

                # Check if the hardlink already exists
                if os.path.exists(dest_file):
                    print(f"{timestamp()} - Hardlink already exists: {os.path.relpath(dest_file, dest_dir)}")
                    continue

                # Create a hardlink
                os.link(src_file, dest_file)
                print(f"{timestamp()} - Created hardlink: {os.path.relpath(dest_file, dest_dir)}")

        else:
            print(f"{timestamp()} - Skipping directory {relative_root} (does not have exactly 1 or 2 files)")

            
if __name__ == "__main__":
    src_directory = "/media/diego/downloads/complete/diego-videos/Football"
    dest_directory = "/media/diego/downloads/complete/diego-videos/Football-hardlinks-debug"

    posters_directory = "/home/diego/htpc-download-box/psg_merger/posters2"
    teams_file = "/home/diego/htpc-download-box/psg_merger/teamnames.txt"
    
    create_hardlinks(src_directory, dest_directory)
