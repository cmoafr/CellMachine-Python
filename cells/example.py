from cell_manager import BaseCell

def load():
    return Example()

# Creating a new cell called Example
class Example(BaseCell):

    def __init__(cell):

        # Name of the texture. REQUIRED
        cell.texture = "example.png"

        # Number of rotations. Optional (Default: 1)
        cell.nb_rotations = 1

        # Update priority (subticking order). Optional (Default: None)
        cell.priority = None

        # Order of appearance of the screen. Higher value = on top.
        # Cells with the same Z order cannot be superposed.
        # Optional (Default: 0)
        cell.z_order = 0

        # Finishing the creation. REQUIRED
        BaseCell.register(cell)
