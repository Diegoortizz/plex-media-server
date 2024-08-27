#!/bin/bash

# Define the two folders
folderA="/media/diego/downloads/complete"
folderB="/media/diego/complete/movies"


# Array to store files to delete and their inodes
declare -A files_to_delete

# Array to store files that didn't find a match in Folder B
unmatched_files=()

# Iterate recursively over each file in Folder A and mark for deletion
while IFS= read -r -d '' fileA; do
    if [ -f "$fileA" ]; then
        # Get the inode of the file in Folder A
        inodeA=$(ls -i "$fileA" | awk '{print $1}')
        filename=$(basename "$fileA")

        # Store the filename and inode in the deletion list
        files_to_delete["$filename"]="$inodeA"
    fi
done < <(find "$folderA" -type f -print0)

# Iterate over the stored files and check for matching inodes in Folder B
for filename in "${!files_to_delete[@]}"; do
    inodeA=${files_to_delete[$filename]}

    # Search for a matching inode in Folder B
    fileB=$(find "$folderB" -type f -inum "$inodeA" 2>/dev/null)
    if [ -n "$fileB" ]; then
        echo " "
        # Confirm deletion from Folder B
        # read -p "Matching file found in $folderB: $fileB. Do you want to delete it? (y/n): " confirm
        # if [[ "$confirm" =~ ^[Yy]$ ]]; then
        #     # rm "$fileB"
        #     echo "Deleted $fileB"
        # else
        #     echo "Skipped deletion of $fileB"
        # fi
    else
        # If no matching file is found, add it to the unmatched files array
        unmatched_files+=("$filename")
        echo "No matching inode found for $filename in $folderB"
    fi
done

# Handle unmatched files in Folder A
if [ ${#unmatched_files[@]} -gt 0 ]; then
    echo "The following files in $folderA did not have matching inodes in $folderB:"
    for filename in "${unmatched_files[@]}"; do
        read -p "Do you want to delete $filename from $folderA? (y/n): " delete_unmatched
        if [[ "$delete_unmatched" =~ ^[Yy]$ ]]; then
            # rm "$folderA/$filename"
            echo "Deleted $folderA/$filename"
        else
            echo "Skipped deletion of $folderA/$filename"
        fi
    done
else
    echo "All files in $folderA had matches in $folderB."
fi

echo "Script finished."
