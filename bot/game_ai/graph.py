import networkx as nx
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from typing import Dict, Tuple, List

from bot.utilities import Point, middle_point, point_convert_to_int
from bot.computer_vision.annotations import AnnotationDrawer
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
    
    def __build_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()

        h_step = (self.screen_size[0] - self.padding) / (self.width-1)
        v_step = (self.screen_size[1] - self.padding+40) / (self.height-1)
        h_border = int(self.padding/2)
        v_border = h_border + 20
        
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
        h_step = (self.screen_size[0] - self.padding) / (self.width-1)
        v_step = (self.screen_size[1] - self.padding+40) / (self.height-1)
        h_border = int(self.padding/2)
        v_border = h_border + 20
        
        middle_x = h_border + int((math.floor(self.width/2) * h_step))
        middle_y = v_border + int((math.floor(self.height/2) * v_step))
        return (middle_x, middle_y)
    
    def draw_to_frame(self, frame):
        drawer = AnnotationDrawer()
        
        for point_a, point_b, data in self.G.edges(data=True):
            cv2.line(frame, point_a, point_b, (255, 255, 255), 2)
            
            weight = data["weight"]
            edge_middle = middle_point(point_a, point_b)
            edge_middle = point_convert_to_int(edge_middle)
            drawer.draw_text_with_background(frame, f"{weight:.2f}", edge_middle)
            
    def draw_solution_to_frame(self, frame, solution):
        for point_a, point_b, _ in solution:
            cv2.line(frame, point_a, point_b, (0, 0, 255), 2)
    
    def draw_network_x(self, evaluator: PositionEvaluator):
        pos= self.__build_network_x_pos()
        edge_labels = self.__get_edge_labels()
        node_labels = self.__get_node_labels(evaluator)

        nx.draw(self.G, pos, with_labels=True, labels=node_labels)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        
        plt.show()
        
    def __build_network_x_pos(self) -> Dict[Point, np.array]:
        pos = {}
        
        for node in self.G.nodes():
            pos[node] = np.array(node)
        return pos
        
    def __get_node_labels(self, evaluator: PositionEvaluator) -> Dict[Point, str]:
        labels = {}
        
        for node, _ in self.G.nodes(data=True):
            labels[node] = f"{evaluator.value(node):.2f}"
        return labels
    
    def __get_edge_labels(self) -> Dict[Point, str]:
        labels = {}
        
        for point_a, point_b, data in self.G.edges(data=True):
            weight = data["weight"]
            labels[(point_a, point_b)] = f"{weight:.2f}"
        return labels
