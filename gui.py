""" The GUI class """

import tkinter as tk
from tkinter import *
from gui_constants import *

class Gui():
    """ Class for drawing a Rubik's Cube using tkinter """
    def __init__(self, root, cube):
        self.root=root
        self.root.title("Rubik's Cube")

        self.canvas=tk.Canvas(root, width=520, height=400, background='white')
        self.canvas.grid(row=0,column=0)
        
        self.cube = cube
        self.cube.draw(self.canvas)
        
        self.root.bind('<f>', self.f_keybind)
        self.root.bind('<r>', self.r_keybind)
        self.root.bind('<u>', self.u_keybind)
        self.root.bind('<l>', self.l_keybind)
        self.root.bind('<b>', self.b_keybind)
        self.root.bind('<d>', self.d_keybind)
        self.root.bind('<m>', self.m_keybind)
        self.root.bind('<e>', self.e_keybind)
        self.root.bind('<s>', self.s_keybind)
        self.root.bind('<x>', self.x_keybind)
        self.root.bind('<y>', self.y_keybind)
        self.root.bind('<z>', self.z_keybind)
        self.root.bind('<F>', self.F_keybind)
        self.root.bind('<R>', self.R_keybind)
        self.root.bind('<U>', self.U_keybind)
        self.root.bind('<L>', self.L_keybind)
        self.root.bind('<B>', self.B_keybind)
        self.root.bind('<D>', self.D_keybind)
        self.root.bind('<M>', self.M_keybind)
        self.root.bind('<E>', self.E_keybind)
        self.root.bind('<S>', self.S_keybind)
        self.root.bind('<X>', self.x_keybind)
        self.root.bind('<Y>', self.y_keybind)
        self.root.bind('<Z>', self.z_keybind)
        
        self.solved_label = tk.Label(self.root, text="Solved")
        self.solved_label.grid(row=1, column=0, pady=20)  
        self.update_solved()

        frame = Frame(self.root)
        frame.grid(row=2, column=0)
        
        for i, (alt_text, rotation) in enumerate(ROTATION_BUTTONS):
            for j, (text, face) in enumerate(FACE_BUTTONS):
                Button(frame, bg='white', text=text+alt_text, command=lambda f=face, r=rotation: self.rotate(f, r)).grid(row=i, column=j)
            for k, (text, axis) in enumerate(AXIS_BUTTONS):
                Button(frame, bg='white', text=text+alt_text, command=lambda a=axis, r=rotation: self.rotate_axis(a, r)).grid(row=i+3, column=k)
            for l, (text, view) in enumerate(VIEW_BUTTONS):
                Button(frame, bg='white', text=text+alt_text, command=lambda v=view, r=rotation: self.view(v, r)).grid(row=i+3, column=l+3)
            for m, (text, double) in enumerate(DOUBLE_BUTTONS):
                Button(frame, bg='white', text=text+alt_text, command=lambda d=double, r=rotation: self.double_turn(d, r)).grid(row=i+6, column=m)

        tk.Label(self.root, text="Options").grid(row=3, column=0, pady=10)
        
        options_frame = Frame(self.root)
        options_frame.grid(row=4, column=0)
        
        Button(options_frame, bg='white', text="Scramble", command=self.scramble).grid(row=0, column=0) 
        
        Button(options_frame, bg='white', text="Reset", command=self.reset).grid(row=0, column=1) 

    
    def update_solved(self):
        if self.cube.is_solved():
            self.solved_label.config(text="Solved")
        else:
            self.solved_label.config(text="Not Solved")
        self.solved_label.update_idletasks()
    
    def rotate(self, face, rotation):
        self.cube.rotate(face, rotation)
        self.cube.draw(self.canvas)
        self.update_solved()
        
    def rotate_axis(self, axis, rotation):
        self.cube.rotate_axis(axis, rotation)
        self.cube.draw(self.canvas)
        self.update_solved()
        
    def view(self, orientation, rotation):
        self.cube.view(orientation, rotation)
        self.cube.draw(self.canvas)
        self.update_solved()
        
    def double_turn(self, double, rotation):
        self.cube.double_turn(double, rotation)
        self.cube.draw(self.canvas)
        self.update_solved()

    def scramble(self):
        self.cube.randomize(50)
        self.cube.draw(self.canvas)
        self.update_solved()
    
    def reset(self):
        self.cube.reset()
        self.cube.draw(self.canvas)
        self.update_solved()
        
    def f_keybind(self, event):
        self.rotate(Face.F, Rotation.CW)
        
    def r_keybind(self, event):
        self.rotate(Face.R, Rotation.CW)
    
    def u_keybind(self, event):
        self.rotate(Face.U, Rotation.CW)
    
    def l_keybind(self, event):
        self.rotate(Face.L, Rotation.CW)
    
    def b_keybind(self, event):
        self.rotate(Face.B, Rotation.CW)
    
    def d_keybind(self, event):
        self.rotate(Face.D, Rotation.CW)
        
    def m_keybind(self, event):
        self.rotate_axis(Axis.M, Rotation.CW)
        
    def e_keybind(self, event):
        self.rotate_axis(Axis.E, Rotation.CW)
        
    def s_keybind(self, event):
        self.rotate_axis(Axis.S, Rotation.CW)
        
    def x_keybind(self, event):
        self.view(Orientation.x, Rotation.CW)
        
    def y_keybind(self, event):
        self.view(Orientation.y, Rotation.CW)
        
    def z_keybind(self, event):
        self.view(Orientation.z, Rotation.CW)
        
    def F_keybind(self, event):
        self.rotate(Face.F, Rotation.CCW)
        
    def R_keybind(self, event):
        self.rotate(Face.R, Rotation.CCW)
    
    def U_keybind(self, event):
        self.rotate(Face.U, Rotation.CCW)
    
    def L_keybind(self, event):
        self.rotate(Face.L, Rotation.CCW)
    
    def B_keybind(self, event):
        self.rotate(Face.B, Rotation.CCW)
    
    def D_keybind(self, event):
        self.rotate(Face.D, Rotation.CCW)
        
    def M_keybind(self, event):
        self.rotate_axis(Axis.M, Rotation.CCW)
        
    def E_keybind(self, event):
        self.rotate_axis(Axis.E, Rotation.CCW)
        
    def S_keybind(self, event):
        self.rotate_axis(Axis.S, Rotation.CCW)
        
    def X_keybind(self, event):
        self.view(Orientation.x, Rotation.CCW)
        
    def Y_keybind(self, event):
        self.view(Orientation.y, Rotation.CCW)
        
    def Z_keybind(self, event):
        self.view(Orientation.z, Rotation.CCW)