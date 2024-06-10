from ultralytics import YOLO
from collections import namedtuple
from typing import Tuple, List


Detection = namedtuple("Detection", ["position", "label", "confidence"])


class ObjectDetector:
    def __init__(self):
        self.model = YOLO("model/best.pt")
        
    def get_detections(self, frame, confidence: float) -> Tuple[List[Detection], List[str]]:
        results = self.model(frame, conf=confidence)[0]
        
        positions = results.boxes.xyxy.cpu().numpy().astype("uint16")
        labels = results.boxes.cls.cpu().numpy().astype("uint8")
        confidences = results.boxes.conf.cpu().numpy()
        class_names = results.names
        
        detections = [Detection(positions[i], labels[i], confidences[i])
                      for i in range(len(positions))]
        return detections, class_names
