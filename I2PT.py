import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import PIL
import subprocess
from comparator import compare_images
import cv2
import os
import time
from init_folders_files import init_folders_files
from image_capture import image_cap
from qr_read import scan_qrcode
from ref_data_sanitize import ref_data_sanitize
from create_ref_data_list import create_ref_data_list
from homography import homography
from opacity_overlay import opacity_overlay
from remove_background import remove_background 
from rembg import remove
from approve_part import approve_part

##initializatio of folders and data files 
#init_folders_files()
#############################################################################################################
#############################################################################################################

#                              functions for initializing instructions and directories  

#############################################################################################################
#############################################################################################################

def display_instructions():
    print("instuctions initializing onto ui for user experience.")
    instruction_title_label = tk.Label(root, text="I͟n͟s͟t͟r͟u͟c͟t͟i͟o͟n͟s͟").place(x=450, y=520)
    #every line is 20px away from the next (vertically)
    tk.Label(root, text="Step 1: Click QR scan to open QR scan window. Make sure camera is connected.").place(x=450, y=545)
    tk.Label(root, text="             Hold steady QR code 3-8 inches away from the camera to capture data. data shold apear in 'QR Code Data' box to the left.").place(x=450, y=565)
    tk.Label(root, text="Step 2: Click capture image to get a live capture. Make sure there are no obstructions or other objects in image captured.").place(x=450, y=585)
    tk.Label(root, text="             If image captured is not good then re-click 'Capture Image'.").place(x=450, y=605)
    tk.Label(root, text="             Captured image and QR data will be used for next steps.").place(x=450, y=625)
    tk.Label(root, text="Step 3: Select the part, from the drop down menu, that you would like to compare your captured image to. Select thresh level.").place(x=450, y=645)
    tk.Label(root, text="             T͟h͟r͟e͟s͟h͟ l͟e͟v͟e͟l͟ e͟x͟p͟l͟a͟i͟n͟e͟d͟:").place(x=450, y=665)
    tk.Label(root, text="             The thresh establishes how sensative you want the comparison algorithm to be.").place(x=470, y=685)
    tk.Label(root, text="             ◦ A low threshold level means the algorithm sensitivity will increase and detect more diffrences on a pixel to pizel level.").place(x=470, y=705)
    tk.Label(root, text="             ◦ A high threshold level means the algorithm sensitivity will decrease and detect less diffrences on a pixel to pizel level.").place(x=470, y=725)
    tk.Label(root, text="             ◦ High threshold levels are better for mechnical parts, Low threshold levels are good for PCB's to compare detail.").place(x=470, y=745)
    tk.Label(root, text="Step 4: Click compare after selecting part and thresh level. When comparison algoreithm runs, the selected part image will apear to the left.").place(x=450, y=765)
    tk.Label(root, text="Step 5: If needed use the scroll feature next to the blended image to compare your capture to the reference image that you selected.").place(x=450, y=785)
    tk.Label(root, text="             These images are aligned using the algorithm, if the algorithm causes distortion, improper reference image was used ").place(x=450, y=805)
    tk.Label(root, text="             If the proper image reference was used, retake the capture. Possible causes for issue could be lighting, orientation, texture, etc.").place(x=450, y=825)
    tk.Label(root, text="Step 6: After analyzing the annotated images from comparison, if the part has no noticable defects then approve part.").place(x=450, y=845)
    tk.Label(root, text="             Approving the part clears the QR code data and appends it to a data list of approved parts.").place(x=450, y=865)
    tk.Label(root, text="             If there was never any QR Data scanned and visible on the text box, then no part information will be appended to the approved list.").place(x=450, y=885)
    tk.Label(root, text="             Clicking the 'approve part' button only appends text and no image data.").place(x=450, y=905)
    tk.Label(root, text="Repeat steps 1-6 for multiple part comparisons.").place(x=450, y=925)
    tk.Label(root, text="Selecting 'Quit' closes the program.").place(x=450, y=945)




#############################################################################################################
#############################################################################################################

#                              functions for sanitizing non .png reference data from directory 

#############################################################################################################
#############################################################################################################

current_user = None
# Define the target directory and size. 
ref_data_directory = 'ref_data'  # directory of ref_data
#target_size = (396, 298) # in pixels 
target_size = (594, 447) # in pixels 
ref_data_sanitize(ref_data_directory, target_size) # converts images indirectory to PNG if not already, and resizes to 396,298


# Function to apply dark mode to the entire app, this function does not work as intended 
def apply_dark_mode():
    # Set the root window background
    root.config(bg="#2E2E2E")
    
    # Apply dark mode to all widgets
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg="#2E2E2E", fg="white")
        elif isinstance(widget, tk.Button):
            widget.config(bg="#3A3A3A", fg="white", activebackground="#555555", activeforeground="#555555")
        elif isinstance(widget, tk.Entry):  
            widget.config(bg="#3A3A3A", fg="white", insertbackground="white")
        elif isinstance(widget, tk.Text):
            widget.config(bg="#3A3A3A", fg="white", insertbackground="white")
        elif isinstance(widget, ttk.Combobox):
            widget.config(background="#3A3A3A", foreground="white", fieldbackground="#3A3A3A", selectbackground="#555555", selectforeground="white")
        elif isinstance(widget, ttk.Button):
            widget.config(style="TButton")
        elif isinstance(widget, tk.Frame):
            widget.config(bg="#2E2E2E")



# Function to display the value of the slider
def show_value(value):
    opacity_label.config(text=f"Slider Value: {value}")     



#############################################################################################################
#############################################################################################################

#                              sign in functionality

#############################################################################################################
#############################################################################################################



def open_username_prompt():
    # Create a new top-level window for sign-in
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("300x150")

    # Label and Entry for Username
    tk.Label(sign_in_window, text="Enter Username:").pack(pady=10)
    username_entry = tk.Entry(sign_in_window)
    username_entry.pack(pady=5)

    # Function to handle the Sign In button click
    def sign_in():
        global current_user  # Declare that we are using the global variable
        username = username_entry.get()

        if username:  # Check if the username is not empty
            current_user = username  # Save the username to the variable 'current_user'
            messagebox.showinfo("Welcome", f"Welcome, {current_user}!")
            sign_in_window.destroy()  # Close the sign-in window after successful login

            # re-Create the menu bar. updating the current user 
            menu_bar = tk.Menu(root)
            # Create a "File" menu
            file_menu = tk.Menu(menu_bar, tearoff=0)
            file_menu.add_command(label="SignIn", command=open_username_prompt)
            file_menu.add_command(label="Change User", command=open_username_prompt)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=root.destroy)
            file_menu.add_command(label=str("Current user: "+ current_user))
            # Add the "File" menu to the menu bar
            menu_bar.add_cascade(label="User", menu=file_menu)
            # Add the menu bar to the window
            root.config(menu=menu_bar)

        else:
            messagebox.showerror("Error", "Please enter a username")

    # Sign In Button
    sign_in_button = tk.Button(sign_in_window, text="Sign In", command=sign_in)
    sign_in_button.pack(pady=20)



    
#############################################################################################################
#############################################################################################################

#                              functions for button actions 

#############################################################################################################
#############################################################################################################


# Function to display message when qr_scan_button is clicked
def qr_scan_button_click():
    messagebox.showinfo("QR Scan", "press Q or ESC to exit camera viewer.")
    
    try:
        #scan_qrcode(3)
        selected_option = zoom_dropdown_var.get()  # Get the selected option from the combobox  
        if selected_option == "1x Zoom":
            scan_qrcode(1)
        
        elif selected_option == "2x Zoom":
            scan_qrcode(2)
        
        elif selected_option == "3x Zoom":
            scan_qrcode(3)
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run qr_read.py: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Failed to run qr_read.py\nqr_read.py not found.")

# Function to display message when capture_image_button is clicked
def capture_image_button_click():
    messagebox.showinfo("Image Capture", "press 'C' to capture!\n\n press Q or ESC to exit.")

    
    try:
        selected_option = zoom_dropdown_var.get()  # Get the selected option from the combobox    
        if selected_option == "1x Zoom":
            image_cap(1,target_size)

        elif selected_option == "2x Zoom":
            image_cap(2,target_size)

        elif selected_option == "3x Zoom":
            image_cap(3,target_size)
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run image_capture.py: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Failed to run image_capture.py\nimage_capture.py not found.")

# Function to display message when compare_part_button is clicked
def compare_part_button_click():
    selected_part_option = part_dropdown_var.get()  # Get the selected option from the combobox
    selected_thresh_option = diff_thresh_dopdown_var.get()

    #path to display the compared part ref nto the ui 
    ref_image = cv2.imread(os.path.join('ref_data/' + selected_part_option + '.png'))#reference image 

    if selected_part_option == "Select Part":
        messagebox.showinfo("Compare", "Error: Select a part!")
        
    else:
        messagebox.showinfo("Compare", "comparing comparator_input_data.jpg to reference!")
        compare_images(selected_part_option, selected_thresh_option)
        diff_create_image_label()
        thresh_create_image_label()
        blended_create_image_label()
        ref_input_create_image_label()     #display the compared part onto the ui 


# Function to display message when approve_part_button is clicked
def approve_part_button_click():
    with open("qr_data.txt", "r") as source_file:
        # Read the source contents of the file
        source_contents = source_file.read()

    if len(source_contents) > 0 and current_user:  # check to see if the source file has data
        approve_part(current_user)


        #messagebox.showinfo("window title", "messege in window!")
        messagebox.showinfo("Part Aproved", "part approved and time stamped. Info appended to approved_parts.txt!") 
        # make wigets as place holders after approved part
        tk.Frame(root, width=target_size[0]+2, height=target_size[1], bg="lightblue").place(x=450, y=37)
        tk.Frame(root,  width=target_size[0], height=target_size[1], bg="lightblue").place(x=1202,y=37)
        tk.Frame(root,  width=target_size[0], height=target_size[1], bg="lightblue").place(x=1202,y=532)
        tk.Frame(root,  width=(target_size[0]/3)+2, height=(target_size[1]/3)+2, bg="lightblue").place(x=190,y=700)

    if current_user == None:
        messagebox.showinfo("Error", "Error! User must be signed in!")

    if len(source_contents) == 0:
        #messagebox.showinfo("window title", "messege in window!")
        messagebox.showinfo("Error", "QR data source file has no contents")
        #tk.Frame(root, width=target_size[0], height=target_size[1], bg="lightblue").place(x=450, y=35)  # Position it at x=450, y=35






#############################################################################################################
#############################################################################################################

#                                            functions to update

#############################################################################################################
#############################################################################################################


def update_qr_data_file_content():
    # Path to the qr_data.txt file to be able to read from the file and diaplay data on gui 
    file_path = "qr_data.txt"  # Change to the path if diffrent .txt file
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            # Update the text widget if content has changed
            if file_content != text_box.get(1.0, tk.END):
                text_box.delete(1.0, tk.END)  # Clear existing text
                text_box.insert(tk.END, file_content)  # Insert updated content
    except FileNotFoundError:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "File not found!")

    # Call this function again after 1000 ms (1 second)
    root.after(1000, update_qr_data_file_content)



def update_blended_image(value):
    opacity_label.config(text=f"Slider Value: {value}") # value of the slider
    last_ref_used = os.path.join("output", "ref_used.png")# Path to the image ref last used 

    if  os.path.exists('output/ref_used.png'):

        ref_image = cv2.imread(os.path.join('output/ref_used.png'))#reference image last used in comparison
        image2 = cv2.imread(os.path.join('captured/data_capture.png'))#current image 
        
        gray1 = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        aligned_img = homography(gray1,gray2) # align image 1 to image 2
        alpha_value = float(value)/100 # create a alpha value float from 0-1 for opacity rating
        blended_images_w_background = opacity_overlay(gray1,aligned_img, alpha_value) #create ablended image 

        blended_create_image_label()
    elif os.path.exists('output/ref_used.png') == False:
        print("Path to last ref image does not exist. Image not found.")







#############################################################################################################
#############################################################################################################

#                               functions to generate image labels  

#############################################################################################################
#############################################################################################################

#function called when making new comparison and when recruired to generate a new image onto UI in runtime
def diff_create_image_label():
    #global global_diffimg, global_threshimg, global_blendedimg
    if  os.path.exists('output/diff.png'):
        # Create a label to display the diff image
        diff_image_path = os.path.join("output", "diff.png")# Path to the image
        image_diff = PhotoImage(file=diff_image_path)  # Load image
        diff_resized_image = image_diff.subsample(1, 1)  # Resize image
        # Create the label with the image and place it at specific coordinates
        diff_image_label = tk.Label(root, image=diff_resized_image)
        diff_image_label.image = diff_resized_image  # Keep a reference to the image
        diff_image_label.place(x=450, y=35)# place the label image on mainwindow
        return diff_image_label.image 
    elif os.path.exists('output/diff.png') == False:
        print("Image output/diff.png not found")
        # make wigets as place holders after approved part
        tk.Frame(root, width=target_size[0]+2, height=target_size[1], bg="lightblue").place(x=450, y=37)

    
#function called when making new comparison and when recruired to generate a new image onto UI in runtime
def thresh_create_image_label():
    if  os.path.exists('output/thresh.png'):
        # Create a label to display the thresh image
        thresh_image_path = os.path.join("output", "thresh.png")# Path to the image
        image_thresh = PhotoImage(file=thresh_image_path)  # Load image
        thresh_resized_image = image_thresh.subsample(1, 1)  # Resize image
        # Create the label with the image and place it at specific coordinates
        thresh_image_label = tk.Label(root, image=thresh_resized_image)
        thresh_image_label.image = thresh_resized_image  # Keep a reference to the image
        thresh_image_label.place(x=1200,y=35) # place the label image on mainwindow
        return thresh_image_label.image
    elif os.path.exists('output/diff.png') == False:
        print("Image output/thresh.png not found")
        # make wigets as place holders after approved part
        tk.Frame(root,  width=target_size[0], height=target_size[1], bg="lightblue").place(x=1202,y=37)

#function called when making new comparison and when recruired to generate a new image onto UI in runtime
def blended_create_image_label():
    if  os.path.exists('output/blended images.png'):
        # Create a label to display the blended image
        blended_image_path = os.path.join("output", "blended images.png")# Path to the image
        image_blended = PhotoImage(file=blended_image_path)  # Load image
        blended_resized_image = image_blended.subsample(1, 1)  # Resize image
        # Create the label with the image and place it at specific coordinates
        blened_image_label = tk.Label(root, image=blended_resized_image)
        blened_image_label.image = blended_resized_image  # Keep a reference to the image
        blened_image_label.place(x=1200,y=530) # place the label image on mainwindow
        return blened_image_label.image
    elif os.path.exists('output/blended images.png') == False:
        print("Image output/diff.png not found")
        # make wigets as place holders after approved part
        tk.Frame(root,  width=target_size[0], height=target_size[1], bg="lightblue").place(x=1202,y=532)

def ref_input_create_image_label():
    if  os.path.exists('output/ref_used.png'):
        # Create a label to display the blended image
        ref_image_path = os.path.join("output", "ref_used.png")# Path to the image
        new_ref_image = PhotoImage(file=ref_image_path)  # Load image
        new_ref_resized_image = new_ref_image.subsample(3, 3)  # Resize image
        # Create the label with the image and place it at specific coordinates
        new_ref_image_label = tk.Label(root, image=new_ref_resized_image)
        new_ref_image_label.image = new_ref_resized_image  # Keep a reference to the image
        new_ref_image_label.place(x=190,y=700) # place the label image on mainwindow
        return new_ref_image_label.image
    elif os.path.exists('output/ref_used.png') == False:
        print("Image output/diff.png not found")
        # make wigets as place holders after approved part
        tk.Frame(root,  width=target_size[0]/3, height=target_size[1]/3, bg="lightblue").place(x=190,y=700)

def delete_image_labels():
    pass
   #global global_diffimg, global_threshimg, global_blendedimg
   #if diff_image_label:
   #    diff_image_label.destroy()
   #    print("Diff image label destroyed")
   #if thresh_image_label:
   #    thresh_image_label.destroy()
   #    print("thresh image label destroyed")
   #if blened_image_label:
   #    blened_image_label.destroy()
   #    print("blended image label destroyed")



#############################################################################################################
#############################################################################################################

#               UI initializations, calls, and placement of labels , images, buttons, values ect.

#############################################################################################################
#############################################################################################################


##og code below

root = Tk() #creating the main window 
root.minsize(1920, 1080)# Set minimum window size to nxn pixels
root.title("I2Tech Part tool")
root.geometry("1920x1080")# geometry of main window 
frm = ttk.Frame(root, padding=10)
frm.grid()

# create logo 
image = PhotoImage(file= os.path.join("logo", "i2Tech-Logomark-3D-Blue.png")) # Load an image for logo
resized_image = image.subsample(11, 11)# Resize the image (this reduces it by a factor)
image_label = tk.Label(root, image=resized_image).place(x=140, y=885)# Create a label widget to hold the image, place the image label onto the window

#display images if they are avaiable from last run of program
print("Displaying images from last program run")
diff_create_image_label()
thresh_create_image_label()
blended_create_image_label()
ref_input_create_image_label()


# re-Create a menu bar. updating the current user 
menu_bar = tk.Menu(root)
# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="SignIn", command=open_username_prompt)
file_menu.add_command(label="Change User", command=open_username_prompt)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
file_menu.add_command(label=str("Current user: None"))
# Add the "File" menu to the menu bar
menu_bar.add_cascade(label="User", menu=file_menu)
# Add the menu bar to the window
root.config(menu=menu_bar)


# create a label 
ttk.Label(frm, text="Q͟R͟ c͟o͟d͟e͟ d͟a͟t͟a͟").place(x=155, y=210)
diff_images_label = tk.Label(root, text="D͟i͟f͟f͟ A͟n͟n͟o͟t͟a͟t͟e͟d͟ o͟n͟ C͟a͟p͟t͟u͟r͟e͟").place(x=700, y=15)
diff_threshhold = tk.Label(root, text="Thresh: ").place(x=310, y=114)
thresh_images_label = tk.Label(root, text="C͟o͟n͟t͟o͟u͟r͟e͟d͟ D͟i͟f͟f͟e͟r͟e͟n͟c͟e͟ T͟h͟r͟e͟s͟h͟o͟l͟d͟ ͟").place(x=1450, y=15)
blended_images_label = tk.Label(root, text="B͟l͟e͟n͟d͟e͟d͟ I͟m͟a͟g͟e͟s͟").place(x=1450, y=500)
last_ref_used = tk.Label(root, text="Selected part last used: ").place(x=50, y=700)


#ttk.Label(frm, text="Camera Zoom setting: ").place(x=300, y=20)

# Create a dropdown zoom (combobox) with options
zoom_options = ["1x Zoom","2x Zoom", "3x Zoom"]
zoom_dropdown_var = StringVar(root)
zoom_dropdown_var.set(zoom_options[0])  # Set the default option
zoom_dropdown_menu = ttk.Combobox(frm, textvariable=zoom_dropdown_var, values=zoom_options, width=8).place(x=110,y=12)



# Create a Text widget to display the file contents
text_box = Text(frm, wrap='word', width=45, height=27)
text_box.grid(column=0, row=5, padx=10, pady=10)


#  function to get ref data for drop down part select
ref_data_list = create_ref_data_list(ref_data_directory) # directory already initialized


# Create a dropdown part select (combobox) with options
part_options = ref_data_list
part_dropdown_var = StringVar(root)
part_dropdown_var.set("Select Part")  # Set the default option
part_dropdown_menu = ttk.Combobox(frm, textvariable=part_dropdown_var, values=part_options).place(x=110,y=103)


# Create a dropdown part select (combobox) with options
diff_thresh_options  = [30, 50, 75, 100, 125, 150, 175, 200]
diff_thresh_dopdown_var = IntVar(root)
diff_thresh_dopdown_var.set(diff_thresh_options[0])  # Set the default option
diff_thresh_dropdown_menu = ttk.Combobox(frm, textvariable=diff_thresh_dopdown_var, values=diff_thresh_options, width=3).place(x=350,y=103)




# Create three buttons and place them in the window
qr_scan_button = ttk.Button(frm, text="QR Scan", command=qr_scan_button_click).grid(column=0, row=0,sticky="w", padx=10, pady=10)

capture_image_button = ttk.Button(frm, text="Capture Image", command=capture_image_button_click).grid(column=0, row=1, sticky="w",padx=10, pady=10)

compare_button = ttk.Button(frm, text="Compare Part", command=compare_part_button_click).grid(column=0, row=2,sticky="w", padx=10, pady=10)

approve_button = ttk.Button(frm, text="Approve part", command=approve_part_button_click).grid(column=0, row=3,sticky="w", padx=10, pady=10)#.place(x=375,y=410)
# the last button is for quiting the program 
quit_button = ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=4, sticky="w",padx=10, pady=10)

# Button to delete the image label, went alternative route instead of deleting images after comaprison, the new comparison generated images are spawned ontop of eachother
#delete_button = tk.Button(root, text="Delete Image", command=delete_image_labels).place(x=450, y=1)


#apply dark mode, uncomment to use, it is still not ready to use 
#apply_dark_mode()

# create slider widget for opacity 
opacity_slider = tk.Scale(root, from_=0, to=100, orient="vertical", command=update_blended_image).place(x=1800,y=700)
# Create a label to show the slider's value
opacity_label = tk.Label(root, text="Slider Value: 0")

display_instructions()

# Start the automatic text box update loop
update_qr_data_file_content()



# Start the main event loop
root.mainloop()

