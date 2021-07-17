class CellType:
    GENERATOR = 0
    CWROTATER = 1
    CCWROTATER = 2
    MOVER = 3
    SLIDE = 4
    BLOCK = 5
    WALL = 6
    ENEMY = 7
    TRASH = 8

class Cell:
    def __init__(self, i, j, type_=None, rotation=0, placeable=False):
        self.x = j
        self.y = i
        self.type = type_
        self.rotation = rotation
        self.placeable = placeable
        
    def isPlaceable(self):
        return self.placeable
    
    def __repr__(self):
        if self.type == None:
            return "."
        for attr in dir(CellType):
            if CellType.__getattribute__(CellType, attr) == self.type:
                return attr + ">v<^"[self.rotation] + "_"*self.placeable
        return "?"

class Cells:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__cellListModif = False
        self.__cellList = []
        self.cellGrid = [[Cell(i, j) for j in range(width)] for i in range(height)]

    def set(self, j, i, type_=None, rotation=0, placeable=False):
        if type(type_) == Cell:
            self.cellGrid[i][j] = type_
        else:
            self.cellGrid[i][j] = Cell(i, j, type_, rotation, placeable)
        self.__cellListModif = True

    @property
    def cellList(self):
        if self.__cellListModif:
            self.__cellList = []
            for i in range(self.height):
                for j in range(self.width):
                    cell = self.cellGrid[i][j]
                    if cell.type != None:
                        self.__cellList.append(cell)
            # => Already sorted
            self.__cellListModif = False
        return self.__cellList

    def __sort(self):
        self.__cellList.sort(key=lambda cell: cell.x+self.width*cell.y)

    def __repr__(self):
        def icon(cell):
            if cell.type == None:
                return " "
            return ")u(nOOOOQQQQ>v<^-|-|++++####@@@@XXXX"[4*cell.type + cell.rotation]
        return "+" + "-"*self.width + "+\n|" + "|\n|".join(reversed(["".join(icon(cell) for cell in line) for line in self.cellGrid])) + "|\n+" + "-"*self.width + "+"
