import os
import zipfile
import pandas as pd
import shutil

# Define the path to the uploaded Excel file and the extraction directory
file_path = 'Амазар_описания 2024.xlsx'
extract_dir = 'extracted_excel'

# Unzip the Excel file to extract its contents
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Define the path for the xl directory and media directory
xl_dir = os.path.join(extract_dir, 'xl')
media_dir = os.path.join(xl_dir, 'media')

# Load the Excel sheet using pandas to get the sample names
sheet_data = pd.read_excel(file_path, sheet_name='Магматические')

# Create folders for the different types of photos
photo_folders = {
    'macro_photo': 'Macro_Photos',
    'straight_light': 'Straight_Light_Photos',
    'reflected_light': 'Reflected_Light_Photos'
}

# Create folders if they don't exist
for folder in photo_folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Get the list of images in the media folder
media_files = sorted(os.listdir(media_dir))

# Initialize the image index to keep track of the current image being processed
image_index = 0
total_images = len(media_files)

# Loop through the sample names and process the images for each sample
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Assuming sample name is in column № (index 4)

    # Process the macro photo (always present)
    if pd.notnull(sample_name) and image_index < total_images:
        macro_img = media_files[image_index]
        shutil.copy(os.path.join(media_dir, macro_img), os.path.join(photo_folders['macro_photo'], f'{sample_name}.jpeg'))
        image_index += 1  # Move to the next image

        # Try to find a straight light photo in the next available image (optional)
        if image_index < total_images:
            straight_light_img = media_files[image_index]
            # Check if the image is likely to be a straight light photo based on its order in the sequence
            if "straight" in straight_light_img.lower() or "light" in straight_light_img.lower():
                shutil.copy(os.path.join(media_dir, straight_light_img), os.path.join(photo_folders['straight_light'], f'{sample_name}.jpeg'))
                image_index += 1  # Move to the next image

        # Try to find a reflected light photo in the next available image (optional)
        if image_index < total_images:
            reflected_light_img = media_files[image_index]
            # Check if the image is likely to be a reflected light photo based on its order
            if "reflected" in reflected_light_img.lower() or "light" in reflected_light_img.lower():
                shutil.copy(os.path.join(media_dir, reflected_light_img), os.path.join(photo_folders['reflected_light'], f'{sample_name}.jpeg'))
                image_index += 1  # Move to the next image

        # Move on to the next sample in the dataset
