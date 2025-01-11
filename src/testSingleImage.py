import os
import cv2
import threading
import queue
import time
import logging
from ultralytics import YOLO
from modules.detect_cars import CarDetector
from modules.plate_detection import LicensePlateDetector
from modules.plate_reader import PlateReader
from modules.register import escreve_no_arquivo
from modules.validatePlate import validate_and_correct_plate
from interface.gui import Interface

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Carregar modelos
model_car = YOLO(os.path.join(ROOT_DIR, 'models', 'front_vehicle.pt'))
model_plate = YOLO(os.path.join(ROOT_DIR, 'models', 'model_plate_recognizer.pt'))
model_characters = YOLO(os.path.join(ROOT_DIR, 'models', 'best.pt'))

# Inicializar detectores
car_detector = CarDetector(model_car)
plate_detector = LicensePlateDetector(model_plate)
plate_reader = PlateReader(model_characters)

dia_folder = 'dia4'
video = 'video8.mp4'

image_path = os.path.join(ROOT_DIR, 'output_frames', dia_folder, f"frame_{video.split('.')[0]}_{dia_folder}.jpg")

image = cv2.imread(image_path)



def testImage(image):
    """
    Process an image to detect cars, license plates, and characters on the plate.
    Args:
        image (numpy.ndarray): Input image to be processed.
    """
    try:
        # Detect cars in the image
        img_with_cars, car_boxes = car_detector.detect_cars(image, drawboxes=False)
        if car_boxes:
            # Extract and resize the first detected vehicle
            vehicle_img = car_detector.extract_and_resize_vehicle(image, car_boxes[0])
            cv2.imshow('Front Vehicle', img_with_cars)

            # Detect license plate in the extracted vehicle image
            imagePlate, plate_boxes = plate_detector.detect_license_plate_box(vehicle_img, drawboxes=False)
            cv2.imshow('License Plate Detection', imagePlate)

            if plate_boxes:
                # Extract and resize the license plate
                plate_img = car_detector.extract_and_resize_vehicle(vehicle_img, plate_boxes[0])

                # Detect characters on the license plate
                imageplate_str, _, plate_str = plate_reader.detect_characters(plate_img, drawboxes=True)
                cv2.imshow('Detected Plate String', imageplate_str)
                logging.info(f"License Plate: {plate_str}")

        else:
            logging.warning("No cars detected in the image.")

    except Exception as e:
        logging.error("Error while processing the frame:", exc_info=True)

    finally:
        # Ensure windows are properly managed
        cv2.waitKey(0)  # Wait for a key press
        cv2.destroyAllWindows()

if image is not None:
    testImage(image)