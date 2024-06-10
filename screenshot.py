import mss
import time
import numpy as np
from typing import Tuple
from mss.screenshot import ScreenShot


def screenshot(bounding_box: Tuple[int, int, int, int]) -> ScreenShot:
    with mss.mss() as sct:
        return np.array(sct.grab(bounding_box))


def grab_every_n_seconds(n: int, bounding_box: Tuple[int, int, int, int]):
    for i in range(0, 100):
        time.sleep(n)
        image = screenshot(bounding_box)
        mss.tools.to_png(image.rgb, image.size, output=f"screenshots/screenshot_{i}.png")

#TODO: Improve screenshot routine with threading
def main():
    """Takes a screenshot every 5 seconds and saves it"""
    bounding_box = (415, 0, 2145, 1080)
    grab_every_n_seconds(5, bounding_box)


if __name__ == "__main__":
    main()
