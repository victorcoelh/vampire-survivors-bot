import cv2
import torch
from typing import List, Tuple

from annotations import AnnotationDrawer
from object_detection import ObjectDetector, Detection
from screenshot import screenshot


def draw_debug_boxes(frame, drawer: AnnotationDrawer,
                     detections: List[Detection], class_names: List[str]):   
    for detection in detections:
        x1, y1, x2, y2 = detection.position
        label = class_names[detection.label]
        debug_info = f"{label}: {detection.confidence:.2f}"
        color = (0, 0, 255) if label == "monster" else (255, 0, 0) # BGR
        
        drawer.draw_rectangle(frame, color, (x1, y1), (x2, y2))
        drawer.draw_text_with_background(frame, debug_info, (x1, y1))


def get_frame_from_game(bounding_box: Tuple[int, int, int, int]):
    frame = screenshot(bounding_box)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    frame = cv2.resize(frame, (960, 608))
    return frame


def main():
    torch.cuda.set_device(0) # Allows PyTorch to use a CUDA GPU for inference.
    drawer = AnnotationDrawer()
    inference_model = ObjectDetector("model/monster_class.pt")
    game_area = {"top": 0, "left": 0, "width": 1245, "height": 768}
    
    while cv2.waitKey(1) != 27:    
        frame = get_frame_from_game(game_area)
        
        detections, class_names = inference_model.get_detections(frame, 0.6)
        draw_debug_boxes(frame, drawer, detections, class_names)
            
        cv2.imshow("Model Vision", frame)
    
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()
