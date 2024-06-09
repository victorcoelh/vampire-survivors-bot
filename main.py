import cv2
import numpy as np
from typing import Tuple

from screenshot import screenshot
from annotations import AnnotationDrawer


def main():
    cv2.namedWindow("Model Vision", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Model Vision", 960, 540)
    bounding_box = (0, 0, 1920, 1080)
    
    drawer = AnnotationDrawer()
    
    while cv2.waitKey(1) != 27:
        frame = np.array(screenshot(bounding_box))
        
        point_a = (300, 300)
        point_b = (600, 600)
        drawer.draw_rectangle(frame, point_a, point_b)
        drawer.draw_text_with_background(frame, "RADIOHEAD", point_a)
        
        cv2.imshow("Model Vision", frame)


if __name__ == "__main__":
    main()
