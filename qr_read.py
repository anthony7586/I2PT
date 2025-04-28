import cv2
from tkinter import messagebox
from dig_zoom_video import dig_zoom_video
import os


def scan_qrcode(zoom_factor):

    #initialize the qr_data.txt file if it does not exist 
    file_name = "qr_data.txt"

    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file if it doesn't exist
        with open(file_name, "w") as file:
            print(f"{file_name} was created successfully.")
    else:
        print(f"{file_name} exists.") #if it exists, just prints out qr_data.txt exists



    # Initialize the camera
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

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


    # Create a window for qr detection 
    window_qr_detection = 'QR detected'
    cv2.namedWindow(window_qr_detection, cv2.WINDOW_NORMAL)
    #set the window height and width    
    cv2.resizeWindow(window_qr_detection, 1624, 1224)  #set at the top of the script, heigh and width is same as resolution ratio 
    
    print(f"Current resolution: {width} x {height}")
    print("Push 'q' or ESC to exit\n\n")


    
    print("Press 'c' to capture an image...")

    while True:
                #Try setting  resolution

        # Read frame from the webcam
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to capture frame")
            break

        # Get the current window size
        window_width, window_height = cv2.getWindowImageRect(window_qr_detection)[2:4]
        
        # Resize the frame to fit the window size
        resized_frame = cv2.resize(frame, (window_width, window_height))
        
        # digital zoom of resized frame, uncomment to zoom frame x2
        resized_frame = dig_zoom_video(resized_frame, zoom_factor)

        # Detect and decode the QR code
        data, bbox, _ = detector.detectAndDecode(resized_frame)
        
        # If a QR code is detected, print the data
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.polylines(resized_frame, [bbox.astype(int)], True, (0, 255, 0), 2)
            if data:
                print(f"QR Code Data:\n{data}")
                with open('qr_data.txt', 'w') as file:
                # Write some text to the file
                    file.write(data)
                    print("\ndata has been written to 'output.txt'")
                    # Release resources
                    cap.release()
                    cv2.destroyAllWindows()
                return data
        

        # Display the boundingbox frame
        cv2.imshow(window_qr_detection, resized_frame)

        #check if key is pressed or window is closed
        key = cv2.waitKey(1) & 0xFF
        
        # Press 'q' to exit or close window 
        if key == ord('q') or  (key == 27):
            print("key pressed. Exiting.")
            break
            
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print("releasing & destroying capture window.")


if __name__ == "__main__":
    scan_qrcode()