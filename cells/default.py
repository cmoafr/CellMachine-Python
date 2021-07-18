from cell_manager import BaseCell

def load():
    return Background()

class Background(BaseCell):

    def __init__(self):
        self.texture = "background.png"
        self.nb_rotations = 1
        self.priority = None
        self.z_order = -100 # /!\ This value is reserved to the background
        BaseCell.register(self)
