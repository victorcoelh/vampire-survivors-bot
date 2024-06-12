import cv2

from bot.computer_vision.object_detection import ObjectDetector
from bot.game_ai.graph import MovementGraph
from bot.game_ai.vampire_bot import PositionEvaluator


def main():
    frame = cv2.imread("screenshots/screenshot_33.png")
    frame = cv2.resize(frame, (960, 540))
    model = ObjectDetector("model/monster_class.pt")

    detections, class_names = model.get_detections(frame, 0.7)
    evaluator = PositionEvaluator(detections, class_names, 1)
    
    G = MovementGraph((960, 540), evaluator)
    G.draw_to_frame(frame)
    
    cv2.imshow("Image", frame)
    cv2.waitKey()
    
"""     image = frame.copy()
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
    cv2.waitKey() """


if __name__ == "__main__":
    main()
