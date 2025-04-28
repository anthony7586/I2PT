import cv2
import numpy as np
import os


def homography(image1,image2):
    ###################################################################################
    # preform homography on image 
    ###################################################################################
    if image1 is None:
        print("Image1 not detected within homography.py")
        exit()
    if image2 is None:
        print("Image2 not detected within homography.py")
        exit()    
               
    # Initialize ORB detector
    orb = cv2.ORB_create(10000)

    # Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)

    # Use FLANN-based matcher for feature matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Sort matches by distance (smaller distance = better match)
    matches = sorted(matches, key=lambda x: x.distance)

    # Extract matched keypoints
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Compute homography matrix using RANSAC
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)

    # Warp image to align with reference
    homography_ouput_img = cv2.warpPerspective(image2, H, (image1.shape[1], image1.shape[0]))


    folder = 'output'
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_filename = os.path.join(folder, 'aligned_capture.png')
    cv2.imwrite(image_filename, homography_ouput_img)  # Save the image

    #cv2.imwrite("homography_ouput.jpg", homography_ouput_img) #saves copy of aligned image 
    print("homography performed on image, image saved as aligned_capture.jpg to output folder")
    #cv2.imshow("aligned_chip.jpg", aligned_img) #display realigned image
    return homography_ouput_img