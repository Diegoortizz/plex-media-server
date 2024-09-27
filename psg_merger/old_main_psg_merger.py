import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def extract_date_and_prefix_from_folder(folder_name):
    # Split the folder name by dots
    parts = folder_name.split('.')
    
    # Find the date part in the list
    for i in range(len(parts)):
        if len(parts[i]) == 4 and parts[i-1].isdigit() and parts[i].isdigit():
            # The date is expected in the format DD.MM.YYYY
            date_str = f"{parts[i-2]}.{parts[i-1]}.{parts[i]}"  # DD.MM.YYYY
            prefix = '.'.join(parts[:i-2])  # Everything before the date
            
            # Replace specific text and format the prefix
            prefix = prefix.replace(".", " ")
            prefix = prefix.replace("-", " vs. ")
            final_string = f"{prefix} - {date_str}"
            final_string = final_string.replace("Foot L1", "").strip()
            
            # Sanitize the final string for use in filenames
            final_string = final_string.replace(":", "-")  # Replace colons in the title
            final_string = final_string.replace("/", "-")  # Replace slashes in the date part
            return final_string
    
    raise ValueError(f"No valid date found in folder name: {folder_name}")


def merge_videos_in_folder(folder_path):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            print(f"{timestamp()} - Processing subfolder: {subfolder}")

            video_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]
            
            if len(video_files) == 2:
                print(f"{timestamp()} - Found 2 video files: {video_files}")

                # Determine which file contains "1" and which contains "2"
                video1 = video_files[0]
                video2 = video_files[1]

                if '1' in video1 and '2' in video2:
                    first_video = video1
                    second_video = video2
                elif '2' in video1 and '1' in video2:
                    first_video = video2
                    second_video = video1
                else:
                    print(f"{timestamp()} - Error: Folder {subfolder} does not contain files named as expected: one with '1' and one with '2'.")
                    continue
                
                # Define file paths
                first_video_path = os.path.join(subfolder_path, first_video)
                second_video_path = os.path.join(subfolder_path, second_video)

                # Extract title and date from folder name
                try:
                    final_title = extract_date_and_prefix_from_folder(subfolder)
                    print(f"{timestamp()} - Extracted title and date: {final_title}")
                except ValueError as e:
                    print(f"{timestamp()} - Error: {e}")
                    continue  # Skip this folder

                # Load video clips
                print(f"{timestamp()} - Loading video clips: {first_video_path} and {second_video_path}")
                clip1 = VideoFileClip(first_video_path)
                clip2 = VideoFileClip(second_video_path)
                
                # Concatenate videos
                print(f"{timestamp()} - Concatenating videos")
                final_clip = concatenate_videoclips([clip1, clip2])
                
                # Extract file extension from the first video
                file_extension = os.path.splitext(first_video)[1]  # Includes the dot (e.g., .mp4)
                
                # Ensure the directory exists
                output_directory = os.path.dirname(os.path.join(subfolder_path, f"{final_title}{file_extension}"))
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                    print(f"{timestamp()} - Created output directory: {output_directory}")
                
                # Save the merged video
                merged_video_path = os.path.join(subfolder_path, f"{final_title}{file_extension}")
                print(f"{timestamp()} - Saving merged video to: {merged_video_path}")
                final_clip.write_videofile(merged_video_path, codec='libx264')
                
                # Close the clips
                clip1.close()
                clip2.close()
                final_clip.close()
                print(f"{timestamp()} - Finished processing subfolder: {subfolder}")
            else:
                print(f"{timestamp()} - Folder {subfolder} does not contain exactly two video files.")
    
    print(f"{timestamp()} - Finished merging process for folder: {folder_path}")

if __name__ == "__main__":
    base_path = '/media/diego/downloads/complete/diego-videos/Football'  # Base path to the directory containing the folder
    # base_path = '/home/diego/htpc-download-box/psg_merger/testfolder'  # Base path to the directory containing the folder
    print(f"{timestamp()} - Starting script")
    merge_videos_in_folder(base_path)
    print(f"{timestamp()} - Script finished")



