raise NotImplementedError("Cells must be redone")

from cell_manager import Cell, CellType

class Saver:

    cellKey = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}"
    def __encode(num):
        if num < len(Saver.cellKey):
            return Saver.cellKey[num]
        encoded = ""
        while num:
            encoded = Saver.cellKey[num%len(Saver.cellKey)] + encoded
            num //= len(Saver.cellKey)
        return encoded



    def saveV3(cells):
        export = "V3;" + Saver.__encode(cells.width) + ";" + Saver.__encode(cells.height) + ";"
        grid_array = [0]*(cells.width*cells.height)
        for i in range(cells.height):
            for j in range(cells.width):
                grid_array[j+i*cells.width] = 73 if cells.cellGrid[i][j].placeable else 72
        for cell in cells.cellList:
            grid_array[cell.x + cell.y*cells.width] += CellType.CCWROTATER * cell.type + 18 * cell.rotation - 72 # ???, CellType.ROTATER = 2
        num3 = 0
        i = 0
        while i < len(grid_array):
            num4 = 0 # Some sort of maximum offset ?
            for j in range(1, i+1):
                num6 = 0 # Some sort of offset ?
                while i + num6 < len(grid_array) and grid_array[i+num6] == grid_array[i+num6-j]:
                    num6 += 1
                    if num6 > num4:
                        num4 = num6
                        num3 = j - 1
            if num4 > 3:
                if len(Saver.__encode(num4)) == 1:
                    if len(Saver.__encode(num3)) == 1:
                        if num4 > 3: # Already tested before. Should be always True ?
                            export += ")" + Saver.__encode(num3) + Saver.__encode(num4)
                            i += num4 - 1
                        else:
                            export += str(Saver.cellKey[grid_array[i]])
                    elif num4 > 3 + len(Saver.__encode(num3)):
                        export += "(" + Saver.__encode(num3) + ")" + Saver.__encode(num4)
                        i += num4 -1
                    else:
                        export += str(Saver.cellKey[grid_array[i]])
                else:
                    export += "(" + Saver.__encode(num3) + "(" + Saver.__encode(num4) + ")"
                    i += num4 - 1
            else:
                export += str(Saver.cellKey[grid_array[i]])
            i += 1
        export += ";;"

        return export



    nb_rotations = {
        CellType.GENERATOR  : 4,
        CellType.CWROTATER  : 1,
        CellType.CCWROTATER : 1,
        CellType.MOVER      : 4,
        CellType.SLIDE      : 2,
        CellType.BLOCK      : 1,
        CellType.WALL       : 1,
        CellType.ENEMY      : 1,
        CellType.TRASH      : 1
    }

    def __getstr(cell, count):
        index = int(cell.placeable) + 10 # +10 because we can't use numbers
        if cell.type != None: # Optimizing by removing unecessary rotations
            index += 2
            for type_ in Saver.nb_rotations:
                mod = Saver.nb_rotations[type_]
                if type_ == cell.type:
                    index += 2 * (cell.rotation % mod)
                    break
                index += 2 * mod
        if count > 1:
            return Saver.cellKey[index] + str(count)
        return Saver.cellKey[index]

    def saveV4(cells):
        export = "V4;" + Saver.__encode(cells.width) + ";" + Saver.__encode(cells.height) + ";"
        for i in range(cells.height):
            if i != 0:
                export += ","
            line = ""
            old = Cell(None, None, None) # Base, empty cell
            count = 0
            for j in range(cells.width):
                cell = cells.cellGrid[i][j]
                if cell.type != old.type or cell.placeable != old.placeable or cell.rotation != old.rotation:
                    if len(line) == 0 and old.type == None:
                        if count > 0:
                            line += str(count)
                    else:
                        line += Saver.__getstr(old, count)
                    old = cell
                    count = 0
                count += 1
            if old.type != None:
                line += Saver.__getstr(old, count)
            export += line
        export += ";;"

        return export



    def save(cells, version=3):
        if version == 1:
            raise ValueError("TODO")
        if version == 2:
            raise ValueError("TODO")
        if version == 3:
            return Saver.saveV3(cells)
        if version == 4:
            return Saver.saveV4(cells)
