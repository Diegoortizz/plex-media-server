import os
import shutil
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def contains_video_file(folder):
    # Check if a folder contains video files with specific extensions
    video_extensions = ['.mkv', '.mp4', '.avi', '.mov']
    for file in os.listdir(folder):
        if any(file.endswith(ext) for ext in video_extensions):
            return True
    return False

def contains_video_file(folder):
    # Check if a folder contains video files with specific extensions
    video_extensions = ['.mkv', '.mp4', '.avi', '.mov']
    for file in os.listdir(folder):
        if any(file.endswith(ext) for ext in video_extensions):
            return True
    return False

def create_hardlinks(src_dir, dest_dir):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over directories in the source directory
    for root, dirs, files in os.walk(src_dir):
        # Get the relative path of the current directory
        relative_root = os.path.relpath(root, src_dir)
        # If the relative path is '.' (i.e., the root directory), skip
        if relative_root == '.':
            continue

        # Create corresponding target directory
        dest_folder = os.path.join(dest_dir, relative_root)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        # List files and count them
        num_files = len(files)
        
        # Process files in the current directory
        for file in files:
            src_file = os.path.join(root, file)
            
            # Compute the target subdirectory and file path based on filename content
            if num_files > 1:
                # Determine the subfolder based on the filename
                if '1' in file:
                    subfolder = os.path.join(dest_folder, '1')
                elif '2' in file:
                    subfolder = os.path.join(dest_folder, '2')
                else:
                    print(f"{timestamp()} - Skipping file: {file} (does not contain '1' or '2')")
                    continue
                
                # Check if the subfolder contains a video file
                if os.path.exists(subfolder) and contains_video_file(subfolder):
                    print(f"{timestamp()} - Skipping subfolder {subfolder} because it already contains a video file.")
                    continue
                
                # Create the subfolder if it does not exist
                if not os.path.exists(subfolder):
                    os.makedirs(subfolder)
                
                dest_file = os.path.join(subfolder, file)
            else:
                # If there's only one file, check the renaming condition
                if 'L1' in file and 'DAZN' in file:
                    # Split the filename to extract team names
                    parts = file.split('.')
                    if len(parts) >= 4:
                        team1 = parts[2]  # Assuming team1 is in the 3rd position
                        team2 = parts[3]  # Assuming team2 is in the 4th position
                        # Extract the file extension
                        file_extension = os.path.splitext(file)[1]
                        # Construct the new filename with the extension
                        new_filename = f"{team1} - {team2} Match complet{file_extension}"
                    else:
                        # Fallback to the original filename if the format is unexpected
                        new_filename = file
                else:
                    # If the filename doesn't contain both "L1" and "DAZN", skip renaming
                    new_filename = file

                dest_file = os.path.join(dest_folder, new_filename)
            
            # Check if the hardlink already exists
            if os.path.exists(dest_file):
                print(f"{timestamp()} - Hardlink already exists: {os.path.relpath(dest_file, dest_dir)}")
                continue    
            
            # Create a hardlink 
            os.link(src_file, dest_file)
            print(f"{timestamp()} - Created hardlink: {os.path.relpath(dest_file, dest_dir)}")


def load_team_aliases(teams_file):
    team_aliases = {}
    with open(teams_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            main_team = parts[0]
            aliases = parts[1:]
            # Map each alias to the main team name
            for alias in aliases:
                team_aliases[alias.lower()] = main_team
            # Map the main team name to itself (in lowercase)
            team_aliases[main_team.lower()] = main_team
    return team_aliases

def get_possible_team_names(team_aliases):
    # Create a set of all possible team names including aliases
    possible_teams = set(team_aliases.keys())
    possible_teams.update({name.lower() for name in team_aliases.values()})
    return possible_teams

def find_teams_in_folder(folder_name, possible_teams):
    found_teams = set()
    for team_name in possible_teams:
        if team_name in folder_name.lower():
            found_teams.add(team_name)
    return found_teams

def assign_posters(video_dir, posters_dir, teams_file):
    # Load team names and possible aliases
    team_aliases = load_team_aliases(teams_file)
    possible_teams = get_possible_team_names(team_aliases)
    
    # Process each directory in the video directory
    for root, dirs, files in os.walk(video_dir):
        # Get the relative path of the current directory
        relative_root = os.path.relpath(root, video_dir)
        
        if relative_root == ".":
            continue

        # Skip directories without files
        if not files:
            print(f"{timestamp()} - No files found in directory: {relative_root}, skipping poster assignment")
            continue
        
        # Find team names in directory names
        found_teams = find_teams_in_folder(relative_root, possible_teams)

        if len(found_teams) >= 2:
            # Find positions of each team in the folder name
            positions = {team: relative_root.lower().find(team) for team in found_teams}
            psg_position = positions.get('psg')
            
            # Determine which team is home and which is away
            if psg_position is not None and len(positions) == 2:
                other_team = [team for team in found_teams if team != 'psg'][0]
                other_team_position = positions[other_team]
                
                # Determine the appropriate poster path based on team positions
                if psg_position < other_team_position:
                    poster_filename = f"PSG-{team_aliases.get(other_team, other_team)}.webp"
                else:
                    poster_filename = f"{team_aliases.get(other_team, other_team)}-PSG.webp"
                
                poster_path = os.path.join(posters_dir, poster_filename)
                
                if os.path.exists(poster_path):
                    # Check if a poster already exists in the directory
                    poster_dest_path = os.path.join(root, 'poster.webp')
                    if not os.path.exists(poster_dest_path):
                        # Copy the poster to the directory
                        shutil.copy(poster_path, poster_dest_path)
                        print(f"{timestamp()} - Copied poster: {poster_filename} to {relative_root}/poster.webp")
                    else:
                        print(f"{timestamp()} - Poster already exists in directory: {relative_root}")
                else:
                    print(f"{timestamp()} - No poster found for directory: {relative_root}")
            else:
                print(f"{timestamp()} - More than two teams or PSG not found in directory name: {relative_root}")
        else:
            print(f"{timestamp()} - Less than two teams found in directory name: {relative_root}")



if __name__ == "__main__":
    src_directory = "/media/diego/downloads/complete/diego-videos/Football"
    dest_directory = "/media/diego/downloads/complete/diego-videos/Football-hardlinks"

    posters_directory = "/home/diego/htpc-download-box/psg_merger/posters2"
    teams_file = "/home/diego/htpc-download-box/psg_merger/teamnames.txt"
    
    create_hardlinks(src_directory, dest_directory)
    assign_posters(dest_directory, posters_directory, teams_file)
