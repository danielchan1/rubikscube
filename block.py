""" The Rubik's Cube Block Class """

import utilities
from enums import *

class Block:
    """ Class representing a generic Rubik's Cube block """
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.block_type = BlockType(utilities.num_zeros_in_coordinates(x, y, z))
        self.initial_colors = self.compute_initial_colors(x, y, z)
        self.colors = self.initial_colors.copy()
        
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})\t{self.block_type}\t\t{', '.join([f'{f}: {c}' for f, c in self.colors.items()])}\n"
    
    def get_x_y_z(self):
        """ returns tuple of coordinates (x, y, z)"""
        return (self.x, self.y, self.z)
    
    def get_x(self):
        """ Returns x coordinate of this block """
        return self.x
    
    def get_y(self):
        """ Returns y coordinate of this block """
        return self.y
    
    def get_z(self):
        """ Returns z coordinate of this block """
        return self.z
    
    def get_block_type(self):
        """ Returns block type of this block """
        return self.block_type

    def get_colors(self, initial=False):
        """ Gets the colors dictionary. If initial is true, returns initial colors """
        return self.initial_colors if initial else self.colors
    
    def get_color(self, face):
        """ Gets the color facing *face* """
        try:
            color = self.colors[face]
        except KeyError:
            color = None
        return color
    
    def get_faces(self):
        """ Given a block, returns tuple of faces that the block is facing"""
        return tuple(self.colors.keys())
    
    def set_color(self, face, color):
        """ Sets the square facing *face* to *color*, returning True on success and False otherwise """
        if (face in self.colors.keys()):
            self.colors[face] = color
            return True
        else:
            return False  
        
    def set_colors(self, face_colors):
        """ Sets the colors dictionary to face_colors """
        self.colors = face_colors.copy()
    
    def is_solved(self):
        """ Does this cube have all of its initial colors facing the correct faces? """
        return all(face.value == color.value for face, color in self.colors.items())
    
    def is_on_face(self, face):
        """ Is block on face? """
        return self.get_x_y_z()[abs(face.value) - 1] == int(face.value / abs(face.value))
    
    def relative_coordinates(self, face):
        """ Coordinates of a block relative to face """
        if not self.is_on_face(face):
            return (0, 0)
        ret = []
        face_tuple = utilities.face_to_tuple(face)
        for index, coordinate in enumerate(self.get_x_y_z()):
            if face_tuple[index] == 0:
                ret.append(coordinate)
        # ret is now [i, j] where i and j are coordinates not represented by face
        match face:
            case Face.B:
                ret[0] *= -1
            case Face.L:
                ret = utilities.new_x_y(tuple(ret), Rotation.CW)
            case Face.R:
                ret = [ret[1], ret[0]]
            case Face.D:
                ret[0] *= -1
            # Face F and Face U are good as-is
        return tuple(ret)
    
    def relative_coordinates_axis(self, axis):
        """ Coordinates of a block relative to an axis """
        (x, y, z) = self.get_x_y_z()
        match axis:
            case Axis.M:
                return (-z, y) if x == 0 else (0, 0)
            case Axis.E:
                return (-x, z) if y == 0 else (0, 0)
            case Axis.S:
                return (x, y) if z == 0 else (0, 0)
            case _:
                return (0, 0)
    
    def get_new_colors(self, face, current_colors):
        """ Gets new colors for self.colors """
        new_face_colors = {current_face: current_color for current_face, current_color in current_colors.items() if current_face == face}
        if self.block_type == BlockType.EDGE:
            other_color = next(current_color for current_face, current_color in current_colors.items() if current_face != face)
            other_face = next(current_face for current_face in self.colors if current_face != face) # buggy!!!
            new_face_colors.update({other_face: other_color})
            return new_face_colors
        elif self.block_type == BlockType.CORNER:
            self_colors = utilities.get_color_corners(self.colors, face)
            self_left = Face(self_colors[CornerColor.LEFT])
            self_right = Face(self_colors[CornerColor.RIGHT])
            left_face = next(current_face for current_face in self.colors if current_face == self_left)
            right_face = next(current_face for current_face in self.colors if current_face == self_right)

            other_colors = utilities.get_color_corners(current_colors, face)
            other_left = Face(other_colors[CornerColor.LEFT])
            other_right = Face(other_colors[CornerColor.RIGHT])
            left_color = current_colors[other_left]
            right_color = current_colors[other_right]
            
            new_face_colors.update({left_face: left_color, right_face: right_color})
            return new_face_colors
        else:
            return dict(self.colors)
    
    def get_new_colors_axis(self, current_colors):
        """ Gets new colors for self.colors for axis rotation """
        if self.block_type == BlockType.MIDDLE:
            new_color = list(current_colors.values())[0]
            new_face = list(self.colors.keys())[0]
            return {new_face: new_color}
        elif self.block_type == BlockType.EDGE:
            shared_face = None
            for self_face in self.colors:
                if self_face in current_colors:
                    shared_face = self_face
                else:
                    self_diff_face = self_face
            for current_face in current_colors:
                if current_face not in self.colors:
                    current_diff_face = current_face
                else:
                    shared_face = current_face
            if not shared_face: # M2 S2 E2
                new_face_colors = {}
                for self_face in self.colors:
                    for current_face in current_colors:
                        if self_face.value == current_face.value * -1:
                            new_face_colors.update({self_face: current_colors[current_face]})
                return new_face_colors
            else:
                return {shared_face: current_colors[current_diff_face], self_diff_face: current_colors[shared_face]}
        else:
            return dict(self.colors)

    @staticmethod
    def compute_initial_colors(x, y, z):
        face_colors = dict()
        if (x):
            face_colors.update({Face(x): Color(x) })
        if (y): 
            face_colors.update({Face(2 * y): Color(2 * y) })
        if (z):
            face_colors.update({Face(3 * z): Color(3 * z) })
        return face_colors
  