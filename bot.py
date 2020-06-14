import random
import networkx as nx
import numpy as np


class Bot:
    def __init__(self, maze):
        self.maze = maze
        self.graph = self.make_graph()

    def make_graph(self):
        g = nx.Graph() # make an empty graph first 
        for x, col in enumerate(self.maze):
            for y, cell  in enumerate(col):
                if cell == 0:
                    g.add_node((x,y))
        for x, y in g.nodes:   #g.node give a list of nodes in the graph
            for neighbor in [(x+1, y), (x, y+1)]:
                if neighbor in g.nodes:
                    g.add_edge((x,y), neighbor)
                    # add line between two nodes
        return g 

##    def valid_moves(self, position):
##        valid = []
##        x, y = position
##        possible_move = {
##            'right': (1, 0),
##            'left': (-1, 0),
##            'up': (0, -1),
##            'down': (0, 1)
##        }
##
##        for key, value in possible_move.items():
##            dx, dy = value 
##            if self.maze[x+dx, y+dy] == 0:
##                valid.append(key)
##        return valid

    def choose_move(self, bone_locations, position):
        closest_bone = None
        for _, point in nx.bfs_edges(self.graph, tuple(position)):
            if point in map(tuple, bone_locations):
                closest_bone = point
                break

        if closest_bone == None:
            return None

        possible_move = {
                (1,0): 'right',
                (-1,0): 'left',
                (0,1): 'down',
                (0,-1): 'up'
        }

        next_move = nx.shortest_path(self.graph,source = tuple(position), target = closest_bone)[1]
        
        move = possible_move[tuple(np.array(next_move) - position)] 
        return move
