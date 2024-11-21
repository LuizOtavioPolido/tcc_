import os
from modules.detect_cars import CarDetector
from modules.plate_detection import LicensePlateDetector
from modules.vertical_projection import VerticalProjection
from modules.plate_reader import PlateReader
import cv2
from ultralytics import YOLO
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

path_model_plate_detector = os.path.join(ROOT_DIR, 'models', 'model_plate_recognizer.pt')
path_default_model_yolo = os.path.join(ROOT_DIR, 'models', 'yolo11s.pt')
path_character_model_yolo = os.path.join(ROOT_DIR, 'models', 'best.pt')
model_plate_detector = YOLO(path_model_plate_detector)
model_default_model_yolo = YOLO(path_default_model_yolo)
model_plate_reader = YOLO(path_character_model_yolo)

def process_image(image_path):
    car_detector = CarDetector(model_default_model_yolo)
    lp_detector = LicensePlateDetector(model_plate_detector)
    reader_plate = PlateReader(model_plate_reader)
    img_with_car_boxes, car_boxes = car_detector.detect_cars(image_path)

    # cv2.imshow('Car Detection', cv2.resize(img_with_car_boxes, (1024, 720)))

    if len(car_boxes) > 0:
        box = car_boxes[0]

        print(f"\nProcessing Vehicle:")

        vehicle_img = car_detector.extract_and_resize_vehicle(img_with_car_boxes, box)
        
        # cv2.imshow('Extracted Vehicle', vehicle_img)

        img_license_plate_box, plate_boxes = lp_detector.detect_license_plate_box(vehicle_img)

        if len(plate_boxes) > 0:
            plate_img = car_detector.extract_and_resize_vehicle(img_license_plate_box, plate_boxes[0])

            if plate_img is not None:
                cv2.imshow('Extracted Vehicle', plate_img)
                img_plate_readed, _, str = reader_plate.detect_characters(plate_img)
                cv2.imshow('Extracted charachteres', img_plate_readed)
                print(f'Placa lida: {str}')
           
        # if license_plate_box:
        #     print(f"License plate box detected: {license_plate_box}")

        #     # Draw bounding box on the vehicle image
        #     img_with_lp_box = lp_detector.draw_bounding_boxes(vehicle_img, [license_plate_box])
            
        #     # Display the image with the bounding box
        #     cv2.imshow('Detected License Plate Box', img_with_lp_box)
        #     cv2.waitKey(0)

        #     # Step 4: Extract the license plate region
        #     x, y, x1, y1 = license_plate_box
        #     plate_region = vehicle_img[y:y1, x:x1]

        #     # Display the extracted plate region
        #     cv2.imshow('Extracted License Plate Region', plate_region)
        #     cv2.waitKey(0)

        #     # Save the final output
        #     output_path = os.path.join(ROOT_DIR, 'output', f'vehicle_result.jpg')
        #     cv2.imwrite(output_path, img_with_lp_box)
        #     print(f"Output saved to: {output_path}")

        else:
            print("Nenhuma placa detectada.")

            
    else:
        print("Nenhum veículo identificado!")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = os.path.join(ROOT_DIR, 'images', '572a11dc0e21634575016c94toyota-prius-2012-com-placa-do-brasil.webp') 

process_image(image_path)

cv2.waitKey(0)
cv2.destroyAllWindows()
