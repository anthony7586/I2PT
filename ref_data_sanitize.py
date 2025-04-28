import os
from PIL import Image

# Define the target directory and size
directory = 'ref_data'
target_size = (396, 298) # in pixels , thia ia for isolated function testing, to change image size refer to I2PT.py file

## this function takes a path and a target size in pixels and converts every image in that directory to a .png of specified size


def ref_data_sanitize(directory, target_size ):

    print("Sanatizing ref data of .jpg, .gif, .jpeg, .bmp files... ")
    # List of file extensions to delete
    extensions_to_delete = ['.jpg', '.jpeg', '.gif', '.bmp']
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's an image file (optional: you can add more extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Check the current size
                    if img.size != target_size:
                        # Resize the image if not already the target size
                        img = img.resize(target_size)
                    
                    # Construct the new file name with .png extension
                    new_file_path = os.path.splitext(file_path)[0] + '.png'
                    
                    # Save the image as .png
                    img.save(new_file_path, 'PNG')
                    print(f'Converted and resized {filename} to {new_file_path}')
                    
                    # Optionally, you can remove the original file after conversion
                    #os.remove(file_path)

            except Exception as e:
                print(f'Error processing {filename}: {e}')

    # Loop through all files in the directory again, deleting all files that are a part of 'extensions to delete'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if the file has one of the specified extensions and is a file
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in extensions_to_delete):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")