import mss
import time
import numpy as np
from typing import Tuple


def screenshot(bounding_box: Tuple[int, int, int, int]) -> np.ndarray:
    with mss.mss() as sct:
        return np.array(sct.grab(bounding_box))


def grab_every_n_seconds(n: int, bounding_box: Tuple[int, int, int, int]):
    for i in range(0, 500):
        time.sleep(n)
        image = screenshot(bounding_box)
        mss.tools.to_png(image.rgb, image.size, output=f"screenshots/screenshot_{i}.png")


def main():
    """Takes a screenshot every 5 seconds and saves it."""
    offset = 70
    bounding_box = (offset, 0, offset+1230, 800)
    grab_every_n_seconds(5, bounding_box)


if __name__ == "__main__":
    main()
