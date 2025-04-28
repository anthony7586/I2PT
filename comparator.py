import cv2
import numpy as np
import os
from homography import homography
from opacity_overlay import opacity_overlay
from remove_background import remove_background 
from rembg import remove
from PIL import Image
import time
from add_hue import add_red_hue



def compare_images(selected_part, selected_thresh_level):
    #retrieve the images
    ref_image = cv2.imread(os.path.join('ref_data/' + selected_part + '.png'))#reference image 
    image2 = cv2.imread(os.path.join('captured/data_capture.png'))#current image 

    #check if image loaded correctly 
    if ref_image is None:
        print("Error: Could not open or find ref_image/image1.")
    if image2 is None:
        print("Error: could not open or find image 2")
    else:



        ###################################################################################
        # preform homography on image to align the PCB or Parts  
        ###################################################################################
        # must have homography.py file in folder for homography  function to be called 
        gray1 = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
              
        #uncomment to display gray1 and gray2 before homography
        #cv2.imshow("homography input gray 2", gray1)
        #cv2.imshow("homography input gray 1", gray2)      
        aligned_img_color = homography(ref_image, image2) # not used but can be used later
        aligned_img = homography(gray1,gray2) # used to calc diff later 

        ###################################################################################
        # background removal using rembg library function (from remg import remove )
        ###################################################################################

        ref_image_no_background = remove_background(ref_image) 
        print("ref background removed ")


        aligned_img_no_background = remove_background(aligned_img)
        print("aligned_img background removed ")

        ###################################################################################
        # preform opacity overlay selected ref image and current image 
        ###################################################################################

        blended_images_no_background = opacity_overlay(ref_image_no_background,aligned_img_no_background, 0.5)
        #the image overlay is dispayed from function and saved in forlder
        #time.sleep(2)  # Delay for n seconds

    
        blended_images_w_background = opacity_overlay(gray1,aligned_img, 0.5)


        ###################################################################################
        # compute difference 
        ###################################################################################
        # explenation of 
        #diff: This is the image where the differences between two images (or frames) are stored. Typically, this is the result of subtracting one image from another, and it highlights the areas where there is a difference.
        #30: This is the threshold value. Any pixel value in the diff image that is greater than or equal to 30 will be considered part of the difference (i.e., it's considered significant).
        #255: This is the value that will be assigned to the pixels that exceed the threshold. So, if a pixel in diff has a value greater than or equal to 30, it will be set to 255 (white).
        #cv2.THRESH_BINARY: This is the thresholding type used. The THRESH_BINARY type means that the image will be converted to a binary image where:
            #-Pixels greater than or equal to the threshold value (30) are set to 255 (white).
            #-Pixels less than the threshold value are set to 0 (black).

        # Convert images to grayscale
        gray1 = cv2.cvtColor(ref_image_no_background, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(aligned_img_no_background, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference
        #If a pixel in gray1 has an intensity of 100, and the same pixel in gray2 has an intensity of 130, the difference will be |100 - 130| = 30
        #The result (diff) will be an image where each pixel contains the absolute difference between the grayscale intensities of the two input images.
        diff = cv2.absdiff(gray1, gray2)

        # Apply threshold to highlight differences, line of code below 
        #_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY) # original threshold
        _, thresh = cv2.threshold(diff, selected_thresh_level, 255, cv2.THRESH_BINARY)

        # Find contours of the differences
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around differences around image
        for contour in contours:
            if cv2.contourArea(contour) > 50:  # Ignore small differences, this was originally 50 
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image2, (x, y), (x+w, y+h), (0, 0, 255), 2)
               

        ###################################################################################
        # display windows (ref_image_no_background and threshold diffrence) 
        ###################################################################################
        # Set the desired window size constant, this is used across all windows 
        #window_width, window_height = 800, 600

        #uncomment to show pop up window      
        # Create a window for differences 
        #window1_differences = 'Differences' #set string for window name 
        #cv2.namedWindow(window1_differences, cv2.WINDOW_NORMAL) #set window name 
        #cv2.resizeWindow(window1_differences, window_width, window_height) #set size
        #cv2.imshow(window1_differences, image2)#Display the results window, uncomment to show pop up window   
        # Save the result
        image_filename = os.path.join('output', 'diff.png')
        cv2.imwrite(image_filename, image2)  # Save the image frame, resized frame is only so image is resized to window
        print(f"annotated image saved to {image_filename}")


        #uncomment to show pop up window      
        #creating the 'threshhold differences' window
        #window2_ThreshDiff = 'Threshold Differences'
        #cv2.namedWindow(window2_ThreshDiff, cv2.WINDOW_NORMAL) #set window name 
        #cv2.resizeWindow(window2_ThreshDiff, window_width, window_height) #set size  
        #cv2.imshow(window2_ThreshDiff, thresh)#Display the results window, uncomment to show pop up window   
        # Save the result
        image_filename = os.path.join('output', 'thresh.png')
        cv2.imwrite(image_filename, thresh)  # Save the image frame, resized frame is only so image is resized to window
        print(f"thresh image saved to {image_filename}")

        #uncomment to show pop up window      
        #creating the 'blended image no background' window
        #window3_blended_images_no_background = 'Blended Images (no background)' #set string for window name 
        #cv2.namedWindow(window3_blended_images_no_background, cv2.WINDOW_NORMAL) #set string for window name 
        #cv2.resizeWindow(window3_blended_images_no_background, window_width, window_height) #set size 
        #cv2.imshow(window3_blended_images_no_background, blended_images_no_background) #Display the results window, uncomment to show pop up window   

        #uncomment to show pop up window      
        #creating the 'blended image w background' window
        #window4_blended_images_w_background = 'Blended Images (with background)' #set string for window name 
        #cv2.namedWindow(window4_blended_images_w_background, cv2.WINDOW_NORMAL) #set string for window name 
        #cv2.resizeWindow(window4_blended_images_w_background, window_width, window_height) #set size 
        #cv2.imshow(window4_blended_images_w_background, blended_images_w_background) #Display the results window,    

        #cv2.waitKey(0)
        cv2.destroyAllWindows()
