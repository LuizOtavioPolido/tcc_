import cv2
import numpy as np

def segment_characters(plate_image):
    # Preprocess the plate image for segmentation
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by their x-position (left to right)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    char_images = []
    for contour in contours:
        # Get the bounding box for each character
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small contours that are unlikely to be characters
        if w > 5 and h > 15:
            char_image = plate_image[y:y+h, x:x+w]
            char_images.append(char_image)
    
    return char_images
