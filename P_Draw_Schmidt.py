#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:00:34 2024

@author: jm
"""

import tkinter as tk
from   tkinter import ttk
from   tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from   Sim_Construct    import Construct_Circuit
from   Sim_Exec_Circuit import Exec_Circuit
from   Sim_Draw         import Draw_Circuit, Draw_Schmidt, Draw_Partitions
from   A_Partition_Generator import Von_Neumann_Partitions
from   math import log2
import sys

def checkbox1_changed():
    selected_options = [option for option, var in checkbox1_vars.items() if var.get() == 1]
    print("Selection for set B:", selected_options)

def checkbox2_changed(event):
    for value in values_to_check:
        selected_options = [option for option, var in checkbox2_vars.items() if var.get() == value]
        print(f"Selection for '{value}':", selected_options)

def checkbox3_changed(event):
    selected_option     = checkbox3_vars.get()
    state               = Phis[int(selected_option)]
    vn_partitions       = Von_Neumann_Partitions(state)
    max_schmidt         = max(partition[2][0] for partition in vn_partitions)
    print("Gate #", selected_option)
    for schmidt_rank in range(1, max_schmidt + 1) :
        schmidt_rank_n = []
        for partition in vn_partitions :
            if partition[2][0] == schmidt_rank :
                schmidt_rank_n.append(partition)      
        ordered_partitions.append(schmidt_rank_n)
        if len(schmidt_rank_n) != 0 :
            print("Partitions for Schmidt Rank =", schmidt_rank, ": ", schmidt_rank_n)
    #print(ordered_partitions)
    #print("Partitions pour la Gate #", selected_option, " : ", Von_Neumann_Partitions(Phis[int(selected_option)]))

# Function to update plots based on checkbox state
def update_plots():
    # Clear previous plots
    ax1.clear()
    ax2.clear()

    for widget in frame1.winfo_children():
        widget.destroy()

    # Set plot titles
    ax1.set_title('Circuit')
    ax2.set_title('Entanglement')
    
    ax1.set_yticks(range(-1,NbQubits))
    
    ax1.set_xlim(-4, NbGates+1)
    ax1.set_xticks(range(0,NbGates+1))
    ax2.set_xlim(-4, NbGates+1)
    ax2.set_xticks(range(0,NbGates+1))
    
    A = [option for option, var in checkbox1_vars.items() if var.get() == 0]
    B = [option for option, var in checkbox1_vars.items() if var.get() == 1]
    
    for value in values_to_check:
        selected_options = [option for option, var in checkbox2_vars.items() if var.get() == value]
        print(f"Selection for '{value}':", selected_options)
        
        for option in selected_options:
            index = options_checkbox2.index(option)
            Desc[0][2][index] = value
            
    #print(Desc[0][2])
        
    Draw_Circuit(NbQubits, Desc, A, B, ax1)

    global Phis
    Phis = []
    #global tree
    #global max_schmidt_ranks
    
    (Phis, Rank_VN, Entropy_VN, Rank_SD, Entropy_SD, Max_Schmidt_Ranks, Min_Schmidt_Ranks, Max_VN_Entropy, Min_VN_Entropy) = Exec_Circuit(NbQubits, Desc, A, B, False)
    
    Draw_Schmidt(Rank_VN, Entropy_VN, Max_Schmidt_Ranks, Min_Schmidt_Ranks, Max_VN_Entropy, Min_VN_Entropy, ax2)   

    print(Max_VN_Entropy)

    #print("draw", len(Phis))
    

    # Redraw canvas
    canvas1.draw()
    canvas2.draw()
    Draw_Partitions(frame1, Phis, 12)
    # canvas3.update_idletasks()

def exit() :
    root.destroy()
    sys.exit()

#
#
#   Debut du programme 
#
#
MaxQubits  = 12
Circuit    = 'Exemples/double_bell.txt'

(err, NbQubits, Desc)  = Construct_Circuit (Circuit, MaxQubits)

if not err:
    
    NbGates = len(Desc)
    
    # Initialize tkinter window
    root = tk.Tk()
    root.geometry("")
    root.resizable(True, True)
    root.title('Quantum Circuit and Schmidt Decomposition')

    # Specifiy the adaptative font size
    
    # Initialize matplotlib figures
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    
    # Create canvas for matplotlib figures
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frame1 = tk.Frame(root, borderwidth=0, highlightthickness=0, highlightcolor='white')
    frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Checkbox 1: Individual Selection
    checkbox1_frame = ttk.LabelFrame(root, text="Update Bipartite (Select B) - At least one and not all")
    checkbox1_frame.pack(padx=10, pady=5, fill="both", expand=True)

    options_checkbox1 = []
    options_checkbox2 = []
    for i in range(NbQubits):
        options_checkbox1.append(i)
        options_checkbox2.append(i)

    checkbox1_vars = {}
    i = 0
    for option in options_checkbox1:
        checkbox1_vars[option] = tk.IntVar()
        checkbox1_vars[option].set(i%2)
        i = i + 1
        checkbox = ttk.Checkbutton(checkbox1_frame, text=option, variable=checkbox1_vars[option], command=checkbox1_changed)
        checkbox.pack(side=tk.LEFT, padx=5, pady=2)

    # Checkbox 2: Dropdown Menus
    checkbox2_frame = ttk.LabelFrame(root, text="Qubit inital values (j = -i)")
    checkbox2_frame.pack(padx=10, pady=5, fill="both", expand=True)

    dropdown_values = {}
    values_to_check = ["0", "1", "+", "-", "i", "j"]

    checkbox2_vars = {}
    for option in options_checkbox2:
        dropdown_values[option] = values_to_check
        label = ttk.Label(checkbox2_frame, text=option)
        label.pack(side=tk.LEFT, padx=5, pady=5)

        checkbox2_vars[option] = tk.StringVar()
        checkbox2_vars[option].set(Desc[0][2][option])
        dropdown = ttk.Combobox(checkbox2_frame, values=dropdown_values[option], width=3, textvariable=checkbox2_vars[option])
        dropdown.pack(side=tk.LEFT, padx=5, pady=2)
        dropdown.bind("<<ComboboxSelected>>", checkbox2_changed)

    # Checkbox 3: Choice for entanglement partitions
    #checkbox3_frame = ttk.LabelFrame(root, text="Entanglement Partitions")
    #checkbox3_frame.pack(padx=10, pady=5, fill="both", expand=True)

    #dropdown_values_3 = {}
    #values_gate = []
    #for i in range (NbGates) :
    #    values_gate.append(i)
    
    #dropdown_values_3 = values_gate
    #label = ttk.Label(checkbox3_frame, text="qubit #")
    #label.pack(side=tk.LEFT, padx=5, pady=5)

    #checkbox3_vars = {}
    #checkbox3_vars = tk.StringVar()
    #checkbox3_vars.set("#")
    #dropdown = ttk.Combobox(checkbox3_frame, values=dropdown_values_3, width=3, textvariable=checkbox3_vars)
    #dropdown.pack(side=tk.LEFT, padx=5, pady=2)
    #dropdown.bind("<<ComboboxSelected>>", checkbox3_changed)

    # Confirm and Cancel Buttons
    confirm_button = ttk.Button(root, text="Confirm", command=update_plots)
    confirm_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Quit button (to close the window and shutdown the program)
    exit_button = ttk.Button(root, text="Quit", command=exit)
    exit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Same as above, but for the top right red "X" button
    root.protocol("WM_DELETE_WINDOW", exit)
     
    # Initially update plots based on checkbox state
    update_plots()
    
    # Run tkinter event loop
    root.mainloop()