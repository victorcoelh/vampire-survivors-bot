import time
import threading
from queue import Queue
from typing import List, Tuple
from pynput.keyboard import Controller

from bot.utilities import Point


PLAYER_SPEED = 320 # pixels per second
COMMAND_PIXELS = 75
PATH_QUEUE = Queue()


class PathManager:
    def __init__(self):
        self.input = Controller()
        self.move_time = COMMAND_PIXELS / PLAYER_SPEED
    
    def follow_pathing_queue(self, stop_event: threading.Event):
        while not stop_event.is_set():
            if PATH_QUEUE.qsize() == 0:
                time.sleep(self.move_time)
                continue
            
            next_movement = PATH_QUEUE.get()
            self.input.press(next_movement)
            time.sleep(self.move_time)
            self.input.release(next_movement)
    
    def fpq(self):
        while not PATH_QUEUE.qsize() == 0:               
            next_movement = PATH_QUEUE.get()
            self.input.press(next_movement)
            time.sleep(self.move_time)
            self.input.release(next_movement)
    
    def add_to_pathing_queue(self, movements: List[chr]):
        if PATH_QUEUE.qsize() != 0:
            return False
        for movement in movements:
            PATH_QUEUE.put(movement)
        

def edge_list_to_direction_list(edges: List[Tuple[Point, Point]]):
    directions = []
    for edge in edges:
        point_a, point_b = edge[:2]
        
        if point_b[0] - point_a[0] > 0:
            directions.append('d')
        elif point_b[0] - point_a[0] < 0:
            directions.append('a')
        elif point_b[1] - point_a[1] > 0:
            directions.append('s')
        elif point_b[1] - point_a[1] < 0:
            directions.append('w')
    return directions


if __name__ == "__main__":
    bot = PathManager()
    bot.follow_path_queue()
