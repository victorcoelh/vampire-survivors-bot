from typing import Tuple
import cv2


class AnnotationDrawer:
    def __init__(self,
                 thickness: int = 2,
                 font = cv2.FONT_HERSHEY_SIMPLEX,
                 font_scale = 0.5,
                 font_color = (0, 0, 0)):
        self.thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.font_color = (0, 0, 0)
    
    def draw_rectangle(self, frame, color: Tuple[int, int, int], point_a: Tuple[int, int], point_b: Tuple[int, int]):
        cv2.rectangle(frame, point_a, point_b, color, self.thickness)
        return frame
        
    def draw_text_with_background(self, frame, text: str, point: Tuple[int, int]):
        label_size, base_line = cv2.getTextSize(text, self.font, self.font_scale, 1)
        background_begin = (point[0], point[1] - label_size[1])
        background_end = (point[0] + label_size[0], point[1] + base_line)
        
        cv2.rectangle(frame, background_begin, background_end, (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, text, point, self.font, self.font_scale, self.font_color)
        
        return frame
    
    def draw_performance_stats():
        pass
        