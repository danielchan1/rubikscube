""" The Rubik's Cube class """

import random
import block, utilities
from enums import *
from gui_constants import *

class RubiksCube:
    """ Class representing a 3x3 Rubik's Cube """
    def __init__(self):
        self.blocks = [block.Block(i, j, k) for i in range(-1, 2) for j in range(-1, 2) for k in range(-1, 2)]
                    
    def __repr__(self):
        blocks_str = ""
        for i, block in enumerate(self.get_blocks()):
            blocks_str += f"{block}"
            if (i + 1) % 9 == 0:
                blocks_str += "\n"
        return f"\n{blocks_str}Currently {'solved' if self.is_solved() else 'not solved'}."
    
    def get_blocks(self):
        """ Returns array of Blocks """
        return self.blocks
    
    def get_block(self, x, y, z):
        """ Returns a single block given its coordinates """
        try:
            return next(block for block in self.blocks if block.get_x_y_z() == (x, y, z))
        except StopIteration:
            return None
        
    def get_block_from_face_colors(self, face_colors):
        """ Returns a single block given its colors """
        try:
            return next(block for block in self.blocks if block.get_colors() == face_colors)
        except StopIteration:
            return None
    
    def get_face(self, face):
        """ Returns list of Blocks that are currently on face *face* """
        return [block for block in self.blocks if block.is_on_face(face)]

    def get_axis(self, axis):
        """ Returns list of Blocks that are currently on axis *axis* """
        match axis:
            case Axis.M:
                return [block for block in self.blocks if block.get_x() == 0]
            case Axis.E:
                return [block for block in self.blocks if block.get_y() == 0]
            case Axis.S:
                return [block for block in self.blocks if block.get_z() == 0]
            case _:
                return []

    def reset(self):
        """ Resets all blocks to initial position """
        for block in self.blocks:
            (x, y, z) = block.get_x_y_z()
            block.set_colors(block.compute_initial_colors(x, y, z))

    def white_on_top(self):
        """ Is the white middle square on top? """
        return self.get_block(0, 1, 0).get_color(Face.U) == Color.WHITE
    
    def green_in_front(self):
        """ Is the green middle square in front? """
        return self.get_block(0, 0, -1).get_color(Face.F) == Color.GREEN
    
    def reorient(self):
        """ Reorients cube so white middle is on top, green middle is in front. Returns the moves applied """
        moves = ""
        if not self.white_on_top():
            for face in Face:
                white_middle = self.get_block_from_face_colors({face: Color.WHITE})
                if white_middle:
                    break
            if white_middle.is_on_face(Face.F):
                self.view(Orientation.x, Rotation.CW)
                moves += "x "
            elif white_middle.is_on_face(Face.B):
                self.view(Orientation.x, Rotation.CCW)
                moves += "x' "
            elif white_middle.is_on_face(Face.R):
                self.view(Orientation.z, Rotation.CCW)
                moves += "z' "
            elif white_middle.is_on_face(Face.L):
                self.view(Orientation.z, Rotation.CW)
                moves += "z "
            else:
                self.view(Orientation.x, Rotation.DOUBLE)
                moves += "x2 "
        if not self.green_in_front(): # white should now be on top
            for face in Face:
                green_middle = self.get_block_from_face_colors({face: Color.GREEN})
                if green_middle:
                    break
            if green_middle.is_on_face(Face.L):
                self.view(Orientation.y, Rotation.CCW)
                moves += "y' "
            elif green_middle.is_on_face(Face.R):
                self.view(Orientation.y, Rotation.CW)
                moves += "y "
            else:
                self.view(Orientation.y, Rotation.DOUBLE)
                moves += "y2 "
        return moves
        
    def is_solved(self):
        """ Returns True if the cube is solved, False otherwise. """
        ret = True
        moves = self.reorient().split()
        moves.reverse()
        for block in self.blocks:
            if not block.is_solved():
                ret = False 
        for move in moves:
            self.rotate_from_input(move, reverse=True)
        return ret
    
    def rotate(self, face, rotation):
        """ Rotates face on cube by rotation """
        # print(f"Now rotating {face.name} face - rotation: {rotation.name}")
        blocks_affected = [block for block in self.get_face(face) if not block.get_block_type() == BlockType.MIDDLE]
        todo = {}
        for block in blocks_affected:
            rel = block.relative_coordinates(face)
            new = utilities.new_x_y(rel, rotation)
            (x, y, z) = utilities.absolute_coordinates(new, face)
            from_block = self.get_block(x, y, z)
            new_colors = block.get_new_colors(face, from_block.get_colors())
            todo.update({block: new_colors})
        for block, new_colors in todo.items():
            block.set_colors(new_colors)
            
        if rotation == Rotation.CCW:
            notation = "'"
        elif rotation == Rotation.DOUBLE:
            notation = "2"
        else:
            notation = ""
        return f"{face.name + notation} "
        
    def rotate_axis(self, axis, rotation):
        """ Rotates axis on cube by rotation """
        # print(f"Now rotating {axis.name} axis - rotation: {rotation.name}")
        blocks_affected = [block for block in self.get_axis(axis) if not block.get_block_type() == BlockType.CENTER]
        todo = {}
        for block in blocks_affected:
            rel = block.relative_coordinates_axis(axis)
            new = utilities.new_x_y(rel, rotation)
            (x, y, z) = utilities.absolute_coordinates_axis(new, axis)
            from_block = self.get_block(x, y, z)
            new_colors = block.get_new_colors_axis(from_block.get_colors())
            todo.update({block: new_colors})
        for block, new_colors in todo.items():
            block.set_colors(new_colors)
            
        if rotation == Rotation.CCW:
            notation = "'"
        elif rotation == Rotation.DOUBLE:
            notation = "2"
        else:
            notation = ""
        return f"{axis.name + notation} "
            
    def view(self, orientation, rotation):
        """ Changes the view on the orientation axis """
        match rotation:
            case Rotation.CCW:
                new_ccw_rotation = Rotation.CW
                new_cw_rotation = Rotation.CCW
            case Rotation.CW:
                new_ccw_rotation = Rotation.CCW
                new_cw_rotation = Rotation.CW
            case Rotation.DOUBLE:
                new_ccw_rotation = Rotation.DOUBLE
                new_cw_rotation = Rotation.DOUBLE
        
        match orientation:
            case Orientation.x:
                self.rotate(Face.L, new_ccw_rotation)
                self.rotate_axis(Axis.M, new_ccw_rotation)
                self.rotate(Face.R, new_cw_rotation)
            case Orientation.y:
                self.rotate(Face.U, new_cw_rotation)
                self.rotate_axis(Axis.E, new_ccw_rotation)
                self.rotate(Face.D, new_ccw_rotation)
            case Orientation.z:
                self.rotate(Face.F, new_cw_rotation)
                self.rotate_axis(Axis.S, new_cw_rotation)
                self.rotate(Face.B, new_ccw_rotation)
        
        if rotation == Rotation.CCW:
            notation = "'"
        elif rotation == Rotation.DOUBLE:
            notation = "2"
        else:
            notation = ""
        return f"{orientation.name + notation} "
    
    def double_turn(self, face, rotation):
        """ Rotates two layers at once, face and the axis parallel to it """
        self.rotate(face, rotation)
        axis = next(axis for axis in Axis if axis.value == abs(face.value))
        self.rotate_axis(axis, Rotation.negative(rotation) if face.value > 0 else rotation)
        
        if rotation == Rotation.CCW:
            notation = "'"
        elif rotation == Rotation.DOUBLE:
            notation = "2"
        else:
            notation = ""
        return f"{face.name.lower() + notation} "
                 
    def randomize(self, num_rotations):
        """ Randomizes the cube with num_rotations """
        random.seed()
        log = ""
        random_face = random.choice(list(Face))
        for _ in range(num_rotations):
            random_face = random.choice([face for face in list(Face) if face != random_face])
            random_rotation = random.choice(list(Rotation))
            log += self.rotate(random_face, random_rotation)
        return f"{log}"
    
    def rotate_from_input(self, user_input, reverse=False):
        """ Rotates the cube based on standard rubik's cube notation. Returns success value as boolean """
        if len(user_input) > 2:
            return False
        if len(user_input) == 2 and user_input[-1] == "'":
            move_type = Rotation.CCW if not reverse else Rotation.CW
            move_name = user_input[:-1]  # Remove the apostrophe
        elif len(user_input) == 2 and user_input[-1] == '2':
            move_type = Rotation.DOUBLE
            move_name = user_input[:-1]  # Remove the '2'
        else:
            move_type = Rotation.CW if not reverse else Rotation.CCW
            move_name = user_input
            
        if move_name in [face.name for face in Face]:
            self.rotate(Face[move_name], move_type)
        elif move_name in [face.name.lower() for face in Face]:
            move_name = move_name.upper()
            self.double_turn(Face[move_name], move_type)
        elif move_name in [axis.name for axis in Axis]:
            self.rotate_axis(Axis[move_name], move_type)
        elif move_name in [orientation.name for orientation in Orientation]:
            self.view(Orientation[move_name], move_type)
        else:
            # print(f"{move_name} is not a valid move!")
            return False
        return True
        
    def set_block_colors(self):
        """ Sets the colors for a specific block given user's answers to prompts """ 
        x = int(input("Enter the coordinates of the block you would like to change\nx: "))
        y = int(input("y: "))
        z = int(input("z: "))
        block = self.get_block(x, y, z)
        
        if block.block_type == BlockType.CENTER:
            print("Sorry, that block can not be changed")
            return
        
        faces = block.get_faces()
        for face in faces:
            color = input(f"Set the color facing the {face.name} direction: ").upper()

            while color not in utilities.get_color_names():
                print("Invalid color! Please select one: GREEN, YELLOW, ORANGE, RED, WHITE, BLUE...")
                color = input(f"Set the color facing the {face.name} direction: ").upper()
            
            curr_color = next(c for c in Color if c.name == color or c.name[0] == color)
            block.set_color(face, curr_color)

    def draw(self, canvas):
        """ On canvas, draws each square of the front, top, and side faces according to the color specified in cube """
        faces = [(Face.U, TOP_FACE), (Face.F, FRONTAL_FACE), (Face.R, SIDE_FACE)]
        for (face, face_dict) in faces:
            for coordinates, square in face_dict.items():
                (x, y, z) = coordinates
                color = self.get_block(x, y, z).get_colors()[face]
                points = list(sum(square, ())) # Flatten array of tuples
                canvas.create_polygon(points, outline='#111', fill=color.name, width=3)
