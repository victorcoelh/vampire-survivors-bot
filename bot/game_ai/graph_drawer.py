import networkx as nx
import cv2
import numpy as np
from matplotlib import pyplot as plt
from typing import Dict

from bot.utilities import Point, middle_point, point_convert_to_int
from bot.computer_vision.annotations import AnnotationDrawer
from bot.game_ai.position_evaluator import PositionEvaluator


class GraphDrawer():
    def __init__(self, graph: nx.Graph):
        self.G = graph
    
    def draw_to_frame(self, frame):
        """Overlays the graph on top of an existing image array."""
        drawer = AnnotationDrawer()
        
        for point_a, point_b, data in self.G.edges(data=True):
            cv2.line(frame, point_a, point_b, (255, 255, 255), 2)
            
            weight = data["weight"]
            edge_middle = middle_point(point_a, point_b)
            edge_middle = point_convert_to_int(edge_middle)
            drawer.draw_text_with_background(frame, f"{weight:.2f}", edge_middle)
            
    def draw_solution_to_frame(self, frame, solution):
        """Overlays the solution path on top of an existing image array."""
        for point_a, point_b, _ in solution:
            cv2.line(frame, point_a, point_b, (0, 0, 255), 2)
    
    def draw_network_x(self, evaluator: PositionEvaluator):
        """Plots the given graph on a matplotlib graph."""
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
