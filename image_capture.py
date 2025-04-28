import cv2
import os
from tkinter import messagebox
from dig_zoom_video import dig_zoom_video

def image_cap(zoom_factor,target_size):
    # Initialize Folder where the image will be saved
    folder = 'captured'

    # Create the folder to store image capture if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        messagebox.showinfo("Error", "Error: Could not access camera!\n Make sure camer is connected.")
        return

    #Try setting  resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264) #Attempt to set width to 3264
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448) #Attempt to set height to 2448
    # Get current width and height
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # actual resolution width
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # actual resolution height
    
    # Create a window for image capture  
    window_image_capture = 'Image Capture'
    cv2.namedWindow(window_image_capture, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_image_capture, 1624, 1224)  #set at the top of the script, heigh and width is same as resolution ratio 

    print(f"Current resolution: {width} x {height}")
    print("Push 'q' to exit\n\n")

    print("Press 'c' to capture an image...")

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        
            # Check if the frame was captured successfully
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Get the current window size
        window_width, window_height = cv2.getWindowImageRect(window_image_capture)[2:4]
        # Resize the frame to fit the window size
        resized_frame = cv2.resize(frame, (window_width, window_height))


        # digital zoom of resized frame, uncomment to zoom frame x2
        resized_frame = dig_zoom_video(resized_frame, zoom_factor)


        # Display the frame
        cv2.imshow(window_image_capture, resized_frame)

        # Wait for the 'c' key to capture the image
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):  # Press 'c' to capture the image
            image_filename = os.path.join(folder, 'data_capture.png')
            #cv2.imwrite(image_filename, frame)  # Save the image frame, resized frame is only so image is resized to window
            final_image = cv2.resize(resized_frame, target_size)
            cv2.imwrite(image_filename, final_image)  # Save the image frame, resized frame is only so image is resized to window
            print(f"Image saved to {image_filename}")
            break        
        if (key == 27) or (key == ord('q')):  # Esc key to exit
            print("key pressed. Exiting.")
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
    print("releasing & destroying capture window.")



if __name__ == "__main__":
    image_cap()
