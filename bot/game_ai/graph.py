import networkx as nx
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from typing import Dict

from bot.utilities import Point, middle_point, point_convert_to_int
from bot.computer_vision.annotations import AnnotationDrawer
from bot.game_ai.vampire_bot import PositionEvaluator


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
        v_step = (self.screen_size[1] - self.padding) / (self.height-1)
        borders = int(self.padding/2)
        
        for i in range(self.width):
            for j in range(self.height):
                current = (borders + int(i*h_step), borders + int(j*v_step))
                next_pos = (borders + int((i+1)*h_step), borders + int(j*v_step))         
                edge_value = self.evaluator.value(next_pos) - self.evaluator.value(current)
                       
                if i < self.width-1:
                    if i > (self.width/2)-1:
                        G.add_edge(current, next_pos, weight= edge_value)
                    else:
                        G.add_edge(next_pos, current, weight= -edge_value)
                    
                next_pos = (borders + int(i*h_step), borders + int((j+1)*v_step))	
                edge_value = self.evaluator.value(current) - self.evaluator.value(next_pos)
                
                if j < self.height-1:
                    if j > (self.height/2)-1:
                        G.add_edge(current, next_pos, weight = -edge_value)
                    else:
                        G.add_edge(next_pos, current, weight = edge_value)
            
        return G
    
    def get_middle_node(self) -> Point:
        h_step = (self.screen_size[0] - self.padding) / (self.width-1)
        v_step = (self.screen_size[1] - self.padding) / (self.height-1)
        borders = int(self.padding/2)
        
        middle_x = borders + int((math.floor(self.width/2) * h_step))
        middle_y = borders + int((math.floor(self.height/2) * v_step))
        return (middle_x, middle_y)
    
    def find_highest_value_path(self):
        s = self.get_middle_node()
        assert(self.G.in_degree(s) == 0)
        
        dist = dict.fromkeys(self.G.nodes, -float('inf'))
        dist[s] = 0
        topo_order = nx.topological_sort(self.G)

        for n in topo_order:
            for s in self.G.successors(n):
                if dist[s] < dist[n] + self.G.edges[n,s]['weight']:
                    dist[s] = dist[n] + self.G.edges[n,s]['weight']
        return dist
    
    def draw_to_frame(self, frame):
        drawer = AnnotationDrawer()
        
        for point_a, point_b, data in self.G.edges(data=True):
            cv2.line(frame, point_a, point_b, (255, 255, 255), 2)
            
            weight = data["weight"]
            edge_middle = middle_point(point_a, point_b)
            edge_middle = point_convert_to_int(edge_middle)
            drawer.draw_text_with_background(frame, f"{weight:.2f}", edge_middle)
    
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
