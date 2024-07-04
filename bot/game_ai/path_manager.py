import time
import threading
from queue import Queue
from typing import List, Tuple
from pynput.keyboard import Controller

from bot.utilities import Point


class PathManager:
    def __init__(self, player_speed = 320, pixels_moved = 75):
        self.__path_queue = Queue()
        self.input = Controller()
        self.move_time = pixels_moved / player_speed
    
    def follow_pathing_queue(self, stop_event: threading.Event, pause_event: threading.Event):
        while not stop_event.is_set():
            if self.__path_queue.qsize() == 0 or pause_event.is_set():
                time.sleep(self.move_time)
                continue
            
            print(list(self.__path_queue.queue))
            next_movement = self.__path_queue.get()
            self.input.press(next_movement)
            time.sleep(self.move_time)
            self.input.release(next_movement)
    
    def add_to_pathing_queue(self, movements: List[chr]):
        if self.__path_queue.qsize() != 0:
            return False
        for movement in movements:
            self.__path_queue.put(movement)
        

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
