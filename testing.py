import cv2
import sys
import time
from typing import Tuple

from bot.computer_vision.screenshot import screenshot
from bot.computer_vision.object_detection import ObjectDetector
from bot.game_ai.position_evaluator import PositionEvaluator
from bot.game_ai.graph import MovementGraph
from bot.game_ai.graph_drawer import GraphDrawer


def main():
    """Runs one of the testing methods, based on the first CLI argument passed.

    If testing the evaluation function or the graph implementation, a second CLI
    argument should be passed containing a path to a testing screenshot.
    """
    testing_mode = int(sys.argv[1])
    
    match testing_mode:
        case 1:
            screenshot_path = str(sys.argv[2])
            test_evaluation_function(screenshot_path)
        case 2:
            screenshot_path = str(sys.argv[2])
            test_created_graph(screenshot_path)
        case _:
            bounding_box = (0, 0, 1080, 960)
            find_player_speed(bounding_box)


def test_evaluation_function(screenshot_path: str):
    """Overlays a heatmap with the calculated value of each pixel in the screenshot
    passed as a cli argument.
    """
    frame = cv2.imread(screenshot_path)
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
    

def test_created_graph(screenshot_path: str):
    """Overlays a visual representation of the internal decision-making graph on top
    of the screenshot passed as a cli argument.
    """
    frame = cv2.imread(screenshot_path)
    frame = cv2.resize(frame, (960, 540))
    model = ObjectDetector("model/monster_class.pt")

    detections, class_names = model.get_detections(frame, 0.7)
    evaluator = PositionEvaluator(detections, class_names, 1)
    
    graph = MovementGraph((960, 540), evaluator)
    solution = graph.calculate_best_path(6)
    
    graph_drawer = GraphDrawer(graph.G)
    graph_drawer.draw_to_frame(frame)
    graph_drawer.draw_solution_to_frame(frame, solution)
    
    cv2.imshow("Image", frame)
    cv2.waitKey()


def find_player_speed(bounding_box: Tuple[int, int, int, int], timer: int = 1):
    """Utility tool to help calculate the player's speed."""
    image_1 = screenshot(bounding_box)
    time.sleep(timer)
    image_2 = screenshot(bounding_box)

    image = cv2.add(image_1, image_2)
    cv2.imwrite("speed_test.png", image)


if __name__ == "__main__":
    main()
