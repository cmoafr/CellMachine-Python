import io
import json
import os
from pygame.image import load as load_img



__base_cells = {}
__background = None



class BaseCell:

    def __init__(self, j):
        self.name = j["name"]
        self.texture = load_img("./textures/"+j["texture"])
        self.nb_rotations = j["rotation"]
        self.priorities = j["priority"]
        self.z_order = j["Zorder"] if "Zorder" in j else 0
        if self.z_order == -100 and self.name != "Background":
            raise ValueError(self.name + " has a Z order of -100 but this is reserved for the background")



def register(obj):
    try:
        if type(obj) == str and obj[0] != "{":
            if obj not in os.listdir("./cells"):
                obj = obj + ".json"
            obj = open("./cells/"+obj)
        if type(obj) in (io.BufferedReader, io.TextIOWrapper):
            j = json.load(obj)
        elif type(obj) in (str, bytes):
            j = json.loads(obj)
        __base_cells[j["name"]] = BaseCell(j)
        return
    
    except Exception as e:
        raise RuntimeError("Tried to load an invalid base cell")

def register_all(clear=False):
    global __base_cells, __background
    if clear:
        __base_cells = {}
        __background = None
    for filename in os.listdir("./cells"):
        register(filename)
    for bc in __base_cells.values():
        if bc.z_order == -100:
            __background = bc.texture
            break
    if __background == None:
        raise FileNotFoundError("Background file not found")

def get_background():
    if __background == None:
        raise ValueError("No background defined yet")
    return __background
