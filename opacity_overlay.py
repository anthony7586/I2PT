import cv2
import os



def opacity_overlay(ref_image, overlay, alpha):

    folder = 'output'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
        

    # Resize overlay to match background dimensions (optional)
    overlay = cv2.resize(overlay, (ref_image.shape[1], ref_image.shape[0]))

    # Blend the images with 50% opacity
    alpha #= 0.5  # Opacity level
    blended_images = cv2.addWeighted(ref_image, 1 - alpha, overlay, alpha, 0)

    # make a string of the float so that the value alpha could be ouputed to terminal 
    str_alpha = str(alpha)

    # Save the result
    image_filename = os.path.join(folder, 'blended images.png')
    cv2.imwrite(image_filename, blended_images)  # Save the image frame, resized frame is only so image is resized to window
    print(f"Opacity " + str_alpha +", overlay performed on images, blended opacity Image saved to {image_filename}")

    image_ref_filename = os.path.join(folder, 'ref_used.png')
    cv2.imwrite(image_ref_filename, ref_image)  # Save the image ref, 
    print(f"Ref image saved to {image_ref_filename}")




    return blended_images