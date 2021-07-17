raise NotImplementedError("Cells must be redone")

from cell_manager import Cell, Cells, CellType

class Loader:

    cellKey = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}"
    def __decode(encoded):
        num = 0
        for char in encoded:
            num = len(Loader.cellKey)*num + Loader.cellKey.index(char)
        return num



    def loadV3(code):
        def setcell(c, i):
            if c % 2 == 1:
                cells.set(i%width, i//width, placeable=True)
            if c >= 72:
                return
            cells.set(i%width, i//width, c//2%9, c//18, False)
        array = code.split(";")
        width = Loader.__decode(array[1])
        height = Loader.__decode(array[2])
        cells = Cells(width, height)
        i = 0
        num = 0
        array2 = [0]*(cells.width*cells.height)
        while i < len(array[3]):
            if array[3][i] == ')' or array[3][i] == '(':
                if array[3][i] == ')':
                    i += 2
                    num2 = Loader.__decode(array[3][i-1])
                    num3 = Loader.__decode(array[3][i])
                else:
                    i += 1
                    text = ""
                    while array[3][i] != ')' and array[3][i] != '(':
                        text += array[3][i]
                        i += 1
                    num2 = Loader.__decode(text)
                    if array[3][i] == ')':
                        i += 1
                        num3 = Loader.__decode(array[3][i])
                    else:
                        i += 1
                        text = "";
                        while array[3][i] != ')':
                            text += array[3][i]
                            i += 1
                        num3 = Loader.__decode(text)
                for j in range(num3):
                    setcell(array2[num - num2 - 1], num)
                    array2[num] = array2[num - num2 - 1]
                    num += 1
            else:
                setcell(Loader.__decode(array[3][i]), num)
                array2[num] = Loader.__decode(array[3][i])
                num += 1
            i += 1
        return cells



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

    def __getvalue(char):
        value = Loader.cellKey.index(char) - 12
        if value < 0:
            return None, 0, value == -1
        for type_ in Loader.nb_rotations:
            mod = Loader.nb_rotations[type_]
            if value < 2*mod:
                return type_, int(value/2), bool(value%2)
            value -= 2*mod

    def loadV4(code):
        split = code.split(";")
        width = Loader.__decode(split[1])
        height = Loader.__decode(split[2])
        cells = Cells(width, height)
        lines = split[3].split(",")

        for i in range(len(lines)):
            line = lines[i]
            type_ = None
            rotation = 0
            placeable = False
            j = 0
            count = 0
            for index in range(len(line)):
                char = line[index]
                if char in "0123456789":
                    count = 10*count + int(char)
                else:
                    if index != 0:
                        if not line[index-1] in "0123456789":
                            count = 1
                        for offset in range(count):
                            cells.set(j+offset, i, type_, rotation, placeable)
                        j += count
                        count = 0
                    type_, rotation, placeable = Loader.__getvalue(char)
            if count == 0:
                count = 1
            for offset in range(count):
                cells.set(j+offset, i, type_, rotation, placeable)

        return cells



    def load(code):
        if code.startswith("V1"):
            raise Exception("TODO")
        if code.startswith("V2"):
            raise Exception("TODO")
        if code.startswith("V3"):
            return Loader.loadV3(code)
        if code.startswith("V4"):
            return Loader.loadV4(code)
