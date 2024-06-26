import cv2
import sys
import time
from typing import Tuple

from bot.computer_vision.object_detection import ObjectDetector
from bot.game_ai.graph import MovementGraph
from bot.game_ai.position_evaluator import PositionEvaluator
from bot.computer_vision.screenshot import screenshot


def find_player_speed(bounding_box: Tuple[int, int, int, int], timer: int = 1):
    image_1 = screenshot(bounding_box)
    time.sleep(timer)
    image_2 = screenshot(bounding_box)

    image = cv2.add(image_1, image_2)
    cv2.imwrite("speed_test.png", image)
    
    
def test_evaluation_function():
    frame = cv2.imread("screenshots/screenshot_33.png")
    frame = cv2.resize(frame, (960, 540))
    model = ObjectDetector("model/monster_class.pt")

    detections, class_names = model.get_detections(frame, 0.7)
    evaluator = PositionEvaluator(detections, class_names, 1)

    image = frame.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    height, width, _ = frame.shape
    for i in range(height):
        for j in range(width):
            value = evaluator.value((j, i))
            image[i, j] = int(255*value)
    
    image = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    cv2.imshow("Image", image)
    cv2.waitKey()
    
    image = cv2.add(frame, image)
    cv2.imshow("Image", image)
    cv2.waitKey()


def test_created_graph():
    frame = cv2.imread("screenshots/screenshot_33.png")
    frame = cv2.resize(frame, (960, 540))
    model = ObjectDetector("model/monster_class.pt")

    detections, class_names = model.get_detections(frame, 0.7)
    evaluator = PositionEvaluator(detections, class_names, 1)
    
    G = MovementGraph((960, 540), evaluator)
    solution = G.calculate_best_path(6)
    G.draw_to_frame(frame)
    G.draw_solution_to_frame(frame, solution)
    
    cv2.imshow("Image", frame)
    cv2.waitKey()


def main():
    testing_mode = sys.argv[0]
    
    match testing_mode:
        case 1:
            test_evaluation_function()
        case 2:
            test_created_graph()
        case _:
            find_player_speed()


if __name__ == "__main__":
    main()
