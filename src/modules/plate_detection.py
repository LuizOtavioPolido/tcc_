import cv2
import numpy as np

class LicensePlateDetector:
    def __init__(self, modelLoaded):
        self.modelLoaded = modelLoaded

    def detect_license_plate_box(self, image):
        if image is not None:
            results = self.modelLoaded(image)
            print(results)
            boxes = []

            for result in results:
                for box in result.boxes:

                    x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    
                    # Get class name
                    class_name = self.modelLoaded.names[class_id]
                    
                    # Draw bounding box and label
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
                    cv2.putText(image, f"{class_name} {confidence:.2f}", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                    print(f"{class_name} {confidence:.2f}")
                    boxes.append((x1, y1, x2, y2))

            return image, boxes
