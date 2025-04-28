import cv2

def dig_zoom_video(frame,zoom_factor):

    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Calculate new dimensions for zoomed region
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    
    # Calculate the top-left corner of the zoomed region
    top_x = center_x - new_width // 2
    top_y = center_y - new_height // 2

    # Extract the zoomed region
    zoomed_frame = frame[top_y:top_y + new_height, top_x:top_x + new_width]

    return zoomed_frame