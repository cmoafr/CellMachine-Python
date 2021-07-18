import os
import pygame
from traceback import print_exc



CELL_SIZE = 64

_base_cells = {}
_background = None



class BaseCell:

    texture = None
    nb_rotations = 1
    priority = None
    z_order = 0

    def register(child):
        global _base_cells
        child.name = type(child).__name__
        if child.name == "Example":
            return
        if child.name != "Background" and child.z_order == -100:
            raise ValueError(child.name + " has a Z order of -100 but this is reserved for the background")
        try:
            child.texture = pygame.transform.scale(pygame.image.load("textures/" + child.texture), (CELL_SIZE, CELL_SIZE))
        except FileNotFoundError:
            raise FileNotFoundError("Could not find texture " + child.texture)
        except TypeError:
            raise TypeError(str(child.texture) + " is not a filename")
        except Exception as e:
            raise RuntimeError("An error occured when generating texture for " + child.name)
        _base_cells[child.name] = child



def register_all(clear=False):
    global _base_cells, _background
    if clear:
        _base_cells = {}
        _background = None
    if "default.py" not in os.listdir("cells"):
        raise FileNotFoundError("Default cells not found. Please reinstall the game")
    L = [filename[:-3] for filename in os.listdir("cells") if filename.endswith(".py")]
    for module in L:
        try:
            __import__("cells."+module, fromlist=("load")).load()
        except Exception:
            print("An error occured when loading", filename)
            print_exc()
    for bc in _base_cells.values():
        if bc.z_order == -100:
            _background = bc.texture
            break
    if _background == None:
        raise FileNotFoundError("Background file not found")

def get_background():
    if _background == None:
        raise ValueError("No background defined yet")
    return _background





class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bases = [_base_cells["Background"]]
        self.reset_texture()

    def reset_texture(self):
        texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
        for base in sorted(self.bases, key=lambda base: base.z_order):
            texture.blit(base.texture, (0,0))
        self.texture = texture

    def resize_texture(self, size):
        self.texture = pygame.transform.scale(self.texture, (size, size))





class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__grid = [[Cell(x, y) for y in range(self.width)] for x in range(self.height)]

    def __getitem__(self, coords):
        x, y = coords
        return self.__grid[y][x]

    def resize_textures(self, size):
        for y in range(self.height):
            for x in range(self.width):
                self.__grid[y][x].resize_texture(size)
