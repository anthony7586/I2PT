import os
import shutil

def init_folders_files():
    
    print("\n\n... initializing...\n\n")
    # Initialize the output folder if it does not exist 
    output_folder = os.path.join("output")
    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        print("initializing output directory")
        os.makedirs(output_folder)
        print("output directory initialized successfully.")
    elif os.path.exists(output_folder):
        print("initializing output directory")
        print("output directory exists.")

    #Empties the output folder by removing all files and subfolders.
    print("emptying output directory of files and subdirectories")
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")



    #initialize the qr_data.txt file if it does not exist 
    qr_file = os.path.join("qr_data.txt")
    # Check if the file exists
    print("initializing qr_data.txt file")

    if not os.path.exists(qr_file):
        # Create the file if it doesn't exist
        with open(qr_file, "w") as file:
            print("creating qr_data.txt file")
            file.write("") # empty the file of any residual data 
            print(f"{qr_file} initialized successfully.")
    elif os.path.exists(qr_file):
        print(f"{qr_file} file exists.") #if it exists, just prints out qr_data.txt exists



    # Initialize Folder where captured image will be saved
    captured_folder = os.path.join("captured")
    # Create the folder to store image capture if it doesn't exist
    print("initializing capture directory")
    if not os.path.exists(captured_folder):
        print("creating capture directory")
        os.makedirs(captured_folder)
    elif os.path.exists(captured_folder):
        print("captured directory exists.")



