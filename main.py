""" Main Function """

import tkinter as tk

from enums import *
from gui import Gui
from rubiks_cube import RubiksCube
from utilities import *

QUIT_STRINGS = ["quit", "q", "end", "stop", "exit", "quit!"]
HELP_STRINGS = ["help", "h", "info", "information", "i"]
SCRAMBLE_STRINGS = ["random", "randomize", "shuffle"]
DISPLAY_STRINGS = ["print", "p"]
GUI_STRINGS = ["gui", "g"]
MOVE_STRINGS = ["move", "moves"]
CHANGE_STRINGS = ["change", "c", "manual", "set"]
REVERSE_STRINGS = ["reverse", "rev"]
RESET_STRINGS = ["reset"]
CLEAR_STRINGS = ["clear"]

clear()
cube = RubiksCube()
print("New Rubik's Cube created. Type 'g' to view!")

while True:
    user_input = input("Enter a command (or 'quit' to exit): ").strip()
    
    if user_input.lower() in QUIT_STRINGS:
        if user_input == QUIT_STRINGS[-1] or input("Are you sure? Type 'yes' to confirm: ").strip().lower() == "yes":
            break
    elif user_input.lower() in HELP_STRINGS:
        print("Available commands:")
        print("gui - Show the graphical representation of the cube")
        
        print("F, R, U, L, D, B - Perform clockwise moves on the faces")
        print("F', R', U', L', D', B' - Perform counterclockwise moves on the faces")
        print("F2, R2, U2, L2, D2, B2 - Perform double moves on the faces")
        print("M, M', M2, E, E', E2, S, S', S2 - Perform slice turns")
        print("x, x', x2, y, y', y2, z, z', z2 - Reorient the cube")
        print("f, r, u, l, d, b - Perform double layer turns")
        
        print("random - Scramble the cube. Specify >50 moves to randomize the cube sufficiently.")
        print("print - Display the current cube state in console")
        print("move - Apply a series of moves to the cube")
        print("reverse - Reverse a series of moves")
        print("change - Change the colors of a specific block")
        print("reset - Reset the cube to the initial state")
        print("clear - Clear the console")
        print("quit - Close the program")
    elif user_input.lower() in SCRAMBLE_STRINGS:
        try:
            num_rotations = int(input("Number of moves: "))
            log = cube.randomize(num_rotations)
            print(f"{num_rotations} random moves have been applied:\n{log}")
        except ValueError:
            print("Invalid number.")
    elif user_input.lower() in DISPLAY_STRINGS:
        print(cube)
    elif user_input.lower() in GUI_STRINGS:
        root = tk.Tk()
        gui = Gui(root, cube)
        root.mainloop()
    elif user_input.lower() in MOVE_STRINGS:
        moves = input("Enter one or moves, separated by (space): ").split()
        for move in moves:
            move = remove_braces(move)
            if not cube.rotate_from_input(move):
                print("Invalid move.")
    elif user_input.lower() in CHANGE_STRINGS:
        cube.set_block_colors()
    elif user_input.lower() in REVERSE_STRINGS:
        reverse_moves = input("Enter one or moves, separated by (space): ").split()
        reverse_moves.reverse()
        for move in reverse_moves:
            move = remove_braces(move)
            if not cube.rotate_from_input(move, True):
                print("Invalid move.")
    elif user_input.lower() in RESET_STRINGS:
        cube.reset()
    elif user_input.lower() in CLEAR_STRINGS:
        clear()
    elif any(user_input.lower().startswith(face.name.lower()) for face in Face) or any(user_input.startswith(axis.name) for axis in Axis) or any(user_input.startswith(orientation.name) for orientation in Orientation):
        if not cube.rotate_from_input(user_input):
            print("Invalid move.")
    else:
        print("Invalid command. Type 'help' for available commands.")

