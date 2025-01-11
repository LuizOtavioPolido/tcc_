from ultralytics import YOLO
import cv2
import numpy as np

class PlateReader:
    def __init__(self, modelLoaded):
        self.model = modelLoaded
        print('model jogado pra classe')

    def detect_characters(self, image, drawboxes):
        if image is None:
            print(f"Error: Could not load image {image}")
            return None

        results = self.model(image)
        boxes = []
        
        # print(results)
        plate_str = ''

        # Coletar os dados de cada detecção
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = self.model.names[class_id]
                
                detections.append((x1, y1, x2, y2, class_name, confidence))

        # Ordenar as detecções pela coordenada x1 para garantir a ordem correta
        detections.sort(key=lambda x: x[0])

        # Construir a string da placa na ordem correta e desenhar as caixas
        for x1, y1, x2, y2, class_name, confidence in detections:
            plate_str += class_name

            if drawboxes:   
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"{class_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            boxes.append((x1, y1, x2, y2))

        return image, boxes, plate_str
