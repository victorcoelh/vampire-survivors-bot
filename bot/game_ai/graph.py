import networkx as nx
import cv2

from bot.utilities import Point


class MovementGraph():
    def __init__(self, screen_size: Point, evaluator,
                 width: int = 9, height: int = 7):
        self.screen_size = screen_size
        self.evaluator = evaluator
        self.width = width
        self.height = height
        
        self.G = self.__build_graph()
    
    def __build_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        padding = 100
        print(self.width)
        h_step = (self.screen_size[0] - padding) / (self.width-1)
        v_step = (self.screen_size[1] - padding) / (self.height-1)
        borders = int(padding/2)
        
        for i in range(self.width):
            for j in range(self.height):
                current = (borders + int(i*h_step), borders + int(j*v_step))
                next_pos = (int(current[0]+h_step), int(current[1]))
                edge_value = self.evaluator.value(current) - self.evaluator.value(next_pos)
                
                if i < self.width-1:
                    if i > self.width/2:
                        G.add_edge(current, next_pos, weight= edge_value)
                    else:
                        G.add_edge(next_pos, current, weight= -edge_value)
                    
                next_pos = (int(current[0]), int(current[1]+v_step))	
                edge_value = self.evaluator.value(current) - self.evaluator.value(next_pos)
                
                if j < self.height-1:
                    if j > self.height/2:
                        G.add_edge(current, next_pos, weight = edge_value)
                    else:
                        G.add_edge(next_pos, current, weight = -edge_value)
            
        return G

    def draw_to_frame(self, frame):
        for edge in self.G.edges():
            print(edge)
            cv2.line(frame, edge[0], edge[1], (255, 255, 255), 2)
