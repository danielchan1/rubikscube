""" General utility functions and constants """

from enums import *
from os import system, name

EDGES = [(-1, 0), (0, 1), (1, 0), (0, -1)]
CORNERS = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
FACE_ORDER = [(2, 1, -3), (1, -2, -3), (-3, -2, -1), (-3, -1, 2), (1, 2, 3), (-2, 1, 3), (3, -1, -2), (3, 2, -1)]

def num_zeros_in_coordinates(x, y, z):
    """ Returns the number of zeros among the three inputs"""
    return (1 if x == 0 else 0) + (1 if y == 0 else 0) + (1 if z == 0 else 0)

def face_to_tuple(face):
    """ Returns tuple that corresponds to coordinates of the middle block of face """
    ret = [0, 0, 0]
    ret[abs(face.value) - 1] = int(face.value / abs(face.value))
    return tuple(ret)

def new_x_y(old_x_y, rotation):
    """ Takes relative coordinates for edges or corners as a tuple (x, y) and the rotation as a Rotation enum and returns the new coordinate as a tuple """
    if old_x_y == (0, 0):
        return old_x_y
    is_edge = (old_x_y[0] == 0) or (old_x_y[1] == 0)
    old_index = EDGES.index(old_x_y) if is_edge else CORNERS.index(old_x_y)
    new_index = (old_index - rotation.value) % 4
    return EDGES[new_index] if is_edge else CORNERS[new_index]

def absolute_coordinates(relative_x_y, face):
    """ Returns the inverse of Block.relative_coordinates(face) """ 
    ret = list(relative_x_y)
    match face:
        case Face.B:
            ret[0] *= -1
        case Face.L:
            ret = list(new_x_y(tuple(ret), Rotation.CCW))
        case Face.R:
            ret = [ret[1], ret[0]]
        case Face.D:
            ret[0] *= -1
        # Face F and Face U are good as-is
    face_tuple = next((i, v) for i, v in enumerate(face_to_tuple(face)) if v != 0) # face_tuple = (index of non-zero value v, v)
    ret.insert(face_tuple[0], face_tuple[1])
    return tuple(ret)    

def absolute_coordinates_axis(relative_x_y, axis):
    """ Returns the inverse of Block.relative_coordinates_axis(axis) """
    [x, y] = list(relative_x_y)
    match axis:
        case Axis.M:
            return (0, y, -x)
        case Axis.E:
            return (-x, 0, y)
        case Axis.S:
            return (x, y, 0)
        case _:
            return (0, 0, 0)

def get_color_corners(colors, face):
    """ Gets {LEFT: color, RIGHT: color} dict for a corner, given that block's colors dict """
    faces = list(colors)
    face_tuple = next(face_tuple for face_tuple in FACE_ORDER if faces_match(faces, face_tuple))
    real_order = rotate_face_order(face_tuple, face)
    return { CornerColor.LEFT: real_order[1], CornerColor.RIGHT: real_order[2] }
   
def faces_match(faces, face_tuple):
    """ Determines if given faces match the constant face_tuple"""
    face_values = [val.value for val in faces]
    face_values.sort()
    if face_values == list(face_tuple):
        return True
    face_values.sort(reverse=True)
    return face_values == list(face_tuple)
     
def rotate_face_order(face_order, face):
    """ Rotates face_order tuple so that face is the first index """
    ret = list(face_order)
    while ret[0] != face.value:
        ret.insert(0, ret.pop())
    return ret

def clear():
    """ Clears terminal. Adapted from: https://www.geeksforgeeks.org/clear-screen-python/"""
    system('cls') if name == 'nt' else system('clear')

def get_color_names():
    """ Returns array of color names + initials"""
    color_names = [c.name for c in Color]
    color_initials = [c.name[0] for c in Color]
    return color_names + color_initials

def remove_braces(str):
    """ Removes (), [], {} from given string """
    remove_chars = "()[]{}"
    ret = ""
    for char in str:
        if char not in remove_chars:
            ret += char
    return ret