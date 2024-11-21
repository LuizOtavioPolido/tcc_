import cv2
import pytesseract
import numpy as np

# Load the Haar cascade classifier for license plates from the root directory
plate_cascade = cv2.CascadeClassifier('./haarcascade_russian_plate_number.xml')

# Function to detect and extract the license plate
def detect_license_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect license plates using Haar Cascade
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # If no plates are found, return None
    if len(plates) == 0:
        return image, None
    
    # Take the first detected plate
    x, y, w, h = plates[0]
    plate_image = image[y:y+h, x:x+w]
    
    # Draw rectangle around detected plate
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return image, plate_image

# Function to preprocess the license plate image
def preprocess_plate_image(plate_image):
    # Convert to grayscale
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Otsu's Binarization
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    
    return morph_image

# Function to recognize text from license plate
def recognize_text_from_plate(plate_image):
    # Preprocess plate image
    processed_plate = preprocess_plate_image(plate_image)
    
    # Use pytesseract to recognize text
    custom_config = r'--oem 3 --psm 8'
    plate_text = pytesseract.image_to_string(processed_plate, config=custom_config)
    
    return plate_text.strip()

# Single image path (replace 'your_image.jpg' with the actual image file name)
image_path = 'carro8.jpg'

# Detect license plate
detection_result, plate_roi = detect_license_plate(image_path)

# Check if a plate was detected
if plate_roi is not None:
    # Recognize text from detected license plate
    recognized_text = recognize_text_from_plate(plate_roi)
else:
    recognized_text = "No plate detected"

# Display the detection result
cv2.imshow('Detected Plate', detection_result)
if plate_roi is not None:
    cv2.imshow('Plate ROI', plate_roi)

# Print the recognized text
print(f"Recognized Text: {recognized_text}")

# Wait for key press and close windows
cv2.waitKey(0)
cv2.destroyAllWindows()
