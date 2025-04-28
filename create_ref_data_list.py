import os



def create_ref_data_list(directory_path):
    # Define the path to the "ref_data" directory
    #directory_path = 'ref_data'
    
    # Check if the directory exists
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # List the names of items in the directory
        items = os.listdir(directory_path)
        
        # Store items into a list data structure
        items_list = []
        for item in items:
            filename_without_extension, _ = os.path.splitext(item)
            items_list.append(filename_without_extension)
        
        # Print the list of items
        print("Reference data list: ",items_list)
        return items_list
    else:
        print(f"The directory {directory_path} does not exist or is not a valid directory.")
        print('restart application to re-run ref_data parse')
        return "files not found"
    

#create_ref_data_list(directory_path)
