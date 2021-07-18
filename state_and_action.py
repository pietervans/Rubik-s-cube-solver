from enum import IntEnum, auto
import logging

logging.basicConfig(level = "DEBUG")


class Color(IntEnum):

    ORANGE = auto()
    WHITE = auto()
    RED = auto()
    YELLOW = auto()
    BLUE = auto()
    GREEN = auto()

    def getEscSeqANSI(self, RGB_VALUES = {
                ORANGE: (255,180,100),
                WHITE: (255,255,255),
                RED: (255,0,0),
                YELLOW: (255,255,0),
                BLUE: (50,50,255),
                GREEN: (0,210,0)
            }):
        r,g,b = RGB_VALUES[self]
        return f"\033[38;2;{r};{g};{b}m"


class Action:

    def __init__(self, face, clockwise) -> None:
        self.face = face
        self.clockwise = clockwise
    

    # Map from color to (coordinate index, value)
    # E.g. (0,1) means x=1
    COORDINATES = {
        Color.WHITE: (0,1),
        Color.YELLOW: (0,-1),
        Color.RED: (2,1),
        Color.ORANGE: (2,-1),
        Color.GREEN: (1,1),
        Color.BLUE: (1,-1)
    }

    def getFaceCoordinateValue(self):
        """Return (coordinate index, value)"""
        return Action.COORDINATES[self.face]
    

    def getDataNewPosition(self):
        """Determine data for getNewPosition method"""
        constant_coord_ind = Action.COORDINATES[self.face][0] # E.g. 0 for x=constant
        coord1_ind = 1 if constant_coord_ind==0 else 0
        coord2_ind = 1 if constant_coord_ind==2 else 2
        factor = 1
        if self.clockwise == False:
            factor *= -1
        if (self.face in [Color.YELLOW, Color.ORANGE, Color.GREEN]):
            factor *= -1
        return coord1_ind, coord2_ind, factor

    def getNewPosition(self, position, coord1_ind, coord2_ind, factor):
        """Return the position's x,y,z coordinates after this action"""
        coord1, coord2 = position[coord1_ind], position[coord2_ind]
        temp = factor*coord2
        coord2 = -factor*coord1
        coord1 = temp
        res = list(position)
        res[coord1_ind] = coord1
        res[coord2_ind] = coord2
        return tuple(res)
    

    ORDERING1 = [Color.RED, Color.GREEN, Color.ORANGE, Color.BLUE] # E.g. WHITE clockwise
    ORDERING2 = [Color.WHITE, Color.BLUE, Color.YELLOW, Color.GREEN] # E.g. RED clockwise
    ORDERING3 = [Color.WHITE, Color.RED, Color.YELLOW, Color.ORANGE] # E.g. GREEN clockwise

    # Orderings for clockwise rotation
    ORDERINGS = {
        Color.WHITE: ORDERING1,
        Color.YELLOW: ORDERING1[::-1],
        Color.RED: ORDERING2,
        Color.ORANGE: ORDERING2[::-1],
        Color.GREEN: ORDERING3,
        Color.BLUE: ORDERING3[::-1]
    }

    def getColorDict(self):
        """Return a mapping from colors to colors"""
        ordering = Action.ORDERINGS[self.face][::(1 if self.clockwise else -1)]
        d = dict()
        for i in range(4):
            d[ordering[i]] = ordering[(i+1)%4]
        return d
    
    def __str__(self) -> str:
        return self.face.name + (" Clockwise" if self.clockwise else " Counter-clockwise")


ALL_ACTIONS = [Action(face, True) for face in Color] + [Action(face, False) for face in Color]



class State:

    def __init__(self, positions) -> None:
        """Axes point in the directions:
        x: white, y: green, z: red"""
        self.positions = positions
    
    def isSolved(self) -> bool:
        for elem in self.positions.values():
            if elem.c1 != elem.orientation or elem.c2 != elem.orientation2:
                return False
        return True


    def determineColors(self, side: Color, inv1=1, inv2=1, switch=False):
        """Return color matrix
            side: the color of the side
            inv1, inv2: should coord1/coord2 be inverted?
            switch: should the coordinates be switched?"""
        colors = [
            [0]*3,
            [0, side, 0],
            [0]*3
        ]
        coord_ind, val = Action.COORDINATES[side]
        coord1_ind = 1 if coord_ind==0 else 0
        coord2_ind = 1 if coord_ind==2 else 2
        for pos in self.positions:
            if pos[coord_ind] == val:
                coord1, coord2 = pos[coord1_ind], pos[coord2_ind]
                color = self.positions[pos].getColorOnSide(side)
                if switch:
                    colors[1+inv2*coord2][1+inv1*coord1] = color
                else:
                    colors[1+inv1*coord1][1+inv2*coord2] = color
        return colors

    def getIndentedString(colors, indent=""):
        res = ""
        for row in colors:
            line = "      " + indent
            for c in row:
                line += Color.getEscSeqANSI(c) + "██"
            res += line + "\n"
        return res
    
    def __str__(self):
        res = "\033[1m"
        extra_indent = "   "
        colors_yellow = self.determineColors(Color.YELLOW, switch=True)
        res += State.getIndentedString(colors_yellow, extra_indent)

        colors_red = self.determineColors(Color.RED)
        res += State.getIndentedString(colors_red, extra_indent)

        colors_blue = self.determineColors(Color.BLUE, inv2=-1, switch=True)
        colors_white = self.determineColors(Color.WHITE, inv2=-1, switch=True)
        colors_green = self.determineColors(Color.GREEN, inv1=-1, inv2=-1, switch=True)
        for i in range(3):
            line = extra_indent
            for color_matrix in [colors_blue, colors_white, colors_green]:
                for c in color_matrix[i]:
                    line += Color.getEscSeqANSI(c) + "██"
            res += line + "\n"

        colors_orange = self.determineColors(Color.ORANGE, inv1=-1)
        res += State.getIndentedString(colors_orange, extra_indent)
        
        return res + "\033[39m\033[21m"


class Corner:

    def __init__(self, c1, c2, c3, orientation, orientation2) -> None:
        """c1: reference side, c2: secondary reference side
        ordering of colors does not matter
        orientation: color of center of face of reference side c1
        orientation2: color of center of face of c2"""
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.orientation = orientation
        self.orientation2 = orientation2

    def getColorOnSide(self, side):
        if side == self.orientation:
            return self.c1
        if side == self.orientation2:
            return self.c2
        return self.c3
    

class Edge:

    def __init__(self, c1, c2, orientation, orientation2) -> None:
        """c1: reference side"""
        self.c1 = c1
        self.c2 = c2
        self.orientation = orientation
        self.orientation2 = orientation2 # used to check for goal

    def getColorOnSide(self, side):
        return self.c1 if side==self.orientation else self.c2
