import os

# Specify the path to your folder
folder_path = '/home/diego/htpc-download-box/psg_merger/posters2'

# Mapping of name replacements
name_replacements = {
    '_vs_': '-',
    'MHCS': 'MHSC',
    'OGCN': 'OGC Nice',
    'RCL': 'RC Lens',
    'RCS': 'RCSA',
    'SB': 'SB29',
    'SdR': 'Reims',
    'SR': 'Stade Rennais'
}

# Function to rename files with specific replacements
def rename_files():
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.webp'):
            # Apply _vs_ replacement
            new_name = file_name.replace('_vs_', '-')
            
            # Apply other replacements
            for old_name, new_name_part in name_replacements.items():
                new_name = new_name.replace(old_name, new_name_part)
                
            # Build full file paths
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed: {file_name} -> {new_name}')

# Run the renaming function
rename_files()
