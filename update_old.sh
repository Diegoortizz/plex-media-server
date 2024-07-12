#!/bin/bash

# Get the current date
backup_date=$(date +%Y-%m-%d)

# Get the list of running containers and their details
containers=$(docker ps --format "{{.ID}}\t{{.Names}}")

# Initialize an array to store backup image names
backup_images=()

# Loop through each container to create a backup
echo "Creating backups..."
while IFS=$'\t' read -r container_id container_name; do
    # Skip the header line
    if [ "$container_id" == "CONTAINER" ]; then
        continue
    fi
    
    # Create a backup name with the current date
    backup_name="${container_name}-backup:${backup_date}"
    
    # Commit the container to create a backup image
    echo "Creating backup for container ${container_name} (${container_id}) as ${backup_name}"
    docker commit "$container_id" "$backup_name"
    
    # Add the backup image name to the list for later deletion
    backup_images+=("$backup_name")
done < <(docker ps --format "{{.ID}}\t{{.Names}}")

echo "Backup process completed."

# # Loop through each backup image to delete it
# echo "Deleting backups..."
# for backup_image in "${backup_images[@]}"; do
#     echo "Deleting backup image $backup_image"
#     docker image rm "$backup_image"
# done

# echo "Deletion process completed."

