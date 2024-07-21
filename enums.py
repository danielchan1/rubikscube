""" Enums used throughout the project """

from enum import Enum

class BlockType(Enum):
    """ BlockType.value == # of zeros in (x, y, z) """
    CORNER = 0
    EDGE = 1
    MIDDLE = 2
    CENTER = 3
    
    def __repr__(self):
        return f'{self.name}'
    
    def __format__(self, spec):
        return f'{self.name}'
    
class Face(Enum):
    """ Face.value == sign * |i|, sign == +/- 1 <==> a == (x, y, z) where a[i - 1] != 0 == sign """
    F = -3 # (x, y, -1)
    D = -2 # (x, -1, z)
    L = -1 # (-1, y, z)
    R = 1 # (1, y, z)
    U = 2 # (x, 1, z)
    B = 3 # (x, y, 1)
    
    def __repr__(self):
        return f'{self.name}'
    
    def __format__(self, spec):
        return f'{self.name}'
    
class Axis(Enum):
    """ Middle: Parallel to (L)/R. Equatorial: Parallel to U/(D). Standing: Parallel to  (F)/B """
    M = 1
    E = 2
    S = 3
    
    def __repr__(self):
        return f'{self.name}'
    
    def __format__(self, spec):
        return f'{self.name}'

class Color(Enum):
    """ Color.value == Face.Value for initial state """
    GREEN = -3
    YELLOW = -2
    ORANGE = -1
    RED = 1
    WHITE = 2
    BLUE = 3
    
    def __repr__(self):
        return self.colored()

    def __format__(self, spec):
        return self.colored()
    
    def colored(self):
        """ Returns color text with ASCII escape sequence """
        color_mapping = {
            Color.GREEN: "\x1b[38;5;46mGREEN\x1b[0m",
            Color.YELLOW: "\x1b[38;5;226mYELLOW\x1b[0m",
            Color.ORANGE: "\x1b[38;5;209mORANGE\x1b[0m",
            Color.RED: "\x1b[38;5;196mRED\x1b[0m",
            Color.WHITE: "\x1b[38;5;231mWHITE\x1b[0m",
            Color.BLUE: "\x1b[38;5;33mBLUE\x1b[0m",
        }
        return color_mapping.get(self, f'{self.name}')    

class Rotation(Enum):
    """ Types of rotations """
    CCW = -1
    CW = 1
    DOUBLE = 2
    
    def negative(self):
        """ Inverse rotation """
        if self == Rotation.CCW:
            return Rotation.CW
        elif self == Rotation.CW:
            return Rotation.CCW
        else: # Rotation.DOUBLE
            return self
    
class Orientation(Enum):
    """ Types of cube-reorienting moves. x: rotate the entire cube on R, y: U, z: F """
    x = 1
    y = 2
    z = -3
    
class CornerColor(Enum):
    """ For any block of type CORNER, when looking at face F, the two colors on faces not on F are denoted as LEFT and RIGHT """
    LEFT = 0
    RIGHT = 1
    