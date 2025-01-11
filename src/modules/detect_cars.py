import cv2

class CarDetector:
    def __init__(self, modelLoaded):
        self.modelLoaded = modelLoaded

    def detect_cars(self, frame, drawboxes):
        img = frame
        
        if img is None:
            print(f"Error: Could not load image {frame}")
            return None, []

        results = self.modelLoaded(img)
        boxes = []
        print(results)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = self.modelLoaded.names[class_id]
                
                # Draw bounding box and label
                if drawboxes:
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
                    cv2.putText(img, f"{class_name} {confidence:.2f}", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                boxes.append((x1, y1, x2, y2))

        return img, boxes
    
    def extract_and_resize_vehicle(self, original_img, box, new_size=(1024, 720)):
        x, y, x1, y1 = box
        vehicle = original_img[y:y1, x:x1]
        return cv2.resize(vehicle, new_size)
