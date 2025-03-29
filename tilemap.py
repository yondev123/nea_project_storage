# importing libraries
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Map:
    def __init__(self, filename):
        # this method initialises the map as a list of tiles
        self.data = []
        # gets every line in the file and stores it in data
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * (TILESIZE*2 - 1)
        self.height = self.tileheight * (TILESIZE*2 - 1)
        self.gridwidth = GRIDWIDTH
        self.gridheight = GRIDHEIGHT
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        # this method returns every node within the graph
        return 0 <= node.x < self.gridwidth and 0 <= node.y < self.gridheight

    def passable(self, node):
        # this method returns every node that isn't a wall
        return node not in self.walls

    def find_neighbors(self, node):
        # this method returns the nodes connected to a node
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors
        

class Camera:
    def __init__(self, width, height):
        # this method initialises the camera as a rectangle
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # this method attaches the camera to an object
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # this method updates the camera by defining the x and y coordinates of the camera
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
