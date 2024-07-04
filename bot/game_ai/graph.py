import networkx as nx
import math
from typing import Tuple, List

from bot.utilities import Point
from bot.game_ai.position_evaluator import PositionEvaluator


class MovementGraph():
    def __init__(self, screen_size: Point, evaluator: PositionEvaluator,
                 width: int = 9, height: int = 7, padding: int = 100):
        self.screen_size = screen_size
        self.evaluator = evaluator
        self.width = width
        self.height = height
        self.padding = padding
        self.G = self.__build_graph()
    
    def calculate_best_path(self, turns: int = 5) -> List[Tuple[Point, Point]]:
        current_node = self.get_middle_node()
        path = []
        
        for _ in range(turns):
            out_edges = list(self.G.edges(current_node, data=True))

            if not out_edges:
                print(current_node)
                return path
            
            best_edge = max(out_edges, key= lambda x: x[2]["weight"])
            path.append(best_edge)
            current_node = best_edge[1]
        return path
    
    def get_middle_node(self) -> Point:
        h_step, v_step, h_border, v_border = self.__get_padding()
        
        middle_x = h_border + int((math.floor(self.width/2) * h_step))
        middle_y = v_border + int((math.floor(self.height/2) * v_step))
        return (middle_x, middle_y)
    
    def __build_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        h_step, v_step, h_border, v_border = self.__get_padding()
        
        for i in range(self.width):
            for j in range(self.height):
                current = (h_border + int(i*h_step), v_border + int(j*v_step))
                next_pos = (h_border + int((i+1)*h_step), v_border + int(j*v_step))         
                edge_value = self.evaluator.value(next_pos) - self.evaluator.value(current)
                       
                if i < self.width-1:
                    if i > (self.width/2)-1:
                        G.add_edge(current, next_pos, weight= edge_value)
                    else:
                        G.add_edge(next_pos, current, weight= -edge_value)
                    
                next_pos = (h_border + int(i*h_step), v_border + int((j+1)*v_step))	
                edge_value = self.evaluator.value(current) - self.evaluator.value(next_pos)
                
                if j < self.height-1:
                    if j > (self.height/2)-1:
                        G.add_edge(current, next_pos, weight = -edge_value)
                    else:
                        G.add_edge(next_pos, current, weight = edge_value)
        
        return G

    def __get_padding(self):
        h_step = (self.screen_size[0] - self.padding) / (self.width-1)
        v_step = (self.screen_size[1] - self.padding) / (self.height-1)
        h_border = int(self.padding/2)
        v_border = h_border+10
        
        return h_step, v_step, h_border, v_border
