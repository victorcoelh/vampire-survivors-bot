from typing import List, Dict
from random import sample
import numpy as np

from bot.computer_vision.object_detection import Detection
from bot.utilities import Point, distance_to_point


MAGNET_RANGE = 40
RUNE_VALUE = 0.3
MAX_RISK_DISTANCE = 25


class PositionEvaluator():
    def __init__(self, detections: List[Detection], class_names: Dict[int, str], sampling_rate: float):
        monsters = [(np.mean([x.position[0], x.position[2]]), np.mean([x.position[1], x.position[3]]))
                    for x in detections
                    if class_names[x.label] == "monster"]
        runes = [x.position for x in detections if class_names[x.label] == "rune"]
        
        self.monsters = sample(monsters, int(sampling_rate * len(monsters)))
        self.runes = sample(runes, int(sampling_rate * len(runes)))
        
    def value(self, position: Point) -> float:
        value = 0.5 # base value
        value += self.__gain(position) - self.__risk(position)
        return np.clip(value, 0, 1)
    
    def __gain(self, position: Point):
        runes_collected = [1 - min(0.01*distance_to_point(position, rune), 1)
                           for rune in self.runes]
        
        return sum(runes_collected) * RUNE_VALUE

    #TODO: experiment more with gain and risk functions
    def __risk(self, position: Point):
        closest = np.min([distance_to_point(position, monster)
                          for monster in self.monsters])
        if closest == 0:
            return 99
        
        return MAX_RISK_DISTANCE / closest
