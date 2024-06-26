import cv2
import torch
import pyautogui
import threading
from typing import List, Tuple

from bot.computer_vision.annotations import AnnotationDrawer
from bot.computer_vision.object_detection import ObjectDetector, Detection
from bot.computer_vision.screenshot import screenshot

from bot.game_ai.path_manager import PathManager, edge_list_to_direction_list
from bot.game_ai.position_evaluator import PositionEvaluator
from bot.game_ai.graph import MovementGraph


KEY_ESC = 27
KEY_Q = 113


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


def check_and_update_box_position(key_press, game_area):
    if key_press == KEY_Q:
        x, y = pyautogui.position()
        game_area["top"] = y
        game_area["left"] = x


def main():
    torch.cuda.set_device(0) # Allows PyTorch to use a CUDA GPU for inference.
    drawer = AnnotationDrawer()
    inference_model = ObjectDetector("model/monster_class.pt")
    bot = PathManager()
    
    game_dimensions = (1245, 768)
    game_area = {"top": 0, "left": 0, "width": game_dimensions[0], "height": game_dimensions[1]}

    stop_event = threading.Event()
    bot_thread = threading.Thread(target=bot.follow_pathing_queue, args=[stop_event])
    bot_thread.start()
    
    while (key_press := cv2.waitKey(1)) != KEY_ESC:
        try:
            frame = get_frame_from_game(game_area)
            
            detections, class_names = inference_model.get_detections(frame, 0.6)
            draw_debug_boxes(frame, drawer, detections, class_names)
            
            evaluator = PositionEvaluator(detections, class_names, 1)
            G = MovementGraph((960, 540), evaluator)
            solution = G.calculate_best_path(3)
            G.draw_solution_to_frame(frame, solution)
            
            directions = edge_list_to_direction_list(solution)
            bot.add_to_pathing_queue(directions)
            
            cv2.imshow("Model Vision", frame)
            check_and_update_box_position(key_press, game_area)
        except Exception:
            stop_event.set()
            raise Exception

    stop_event.set()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()
