#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:00:34 2024

@author: jm
"""

import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import matplotlib.patches as patches
from A_Partition_Generator import Von_Neumann_Partitions

def Draw_Circuit(NbQubits, Desc, A, B, ax):
    
    # Create a Rectangle patch for Bipartite
    rect = patches.Rectangle((-2.5, -0.5), 1, NbQubits , linewidth=1, edgecolor='k', facecolor='white')
    ax.add_patch(rect)
    ax.text(-3, NbQubits/2 - 0.5, "Bipartite partition", fontsize=14, rotation=90, ha='center', va='center')
    
    for i in range(NbQubits):
        x1, y1 = [0, len(Desc)+1], [i, i]
        ax.plot (x1, y1, linewidth=0.5, color='black')
        if i in A:
            txt = 'A'
        else:
            txt = 'B'
        ax.text(-2, i, txt, fontsize=12, ha='center', va='center')
    
    InitValues = Desc[0][2]
    for i in range(NbQubits):
        ax.text(-1, i, InitValues[i], fontsize=12, ha='center', va='center')
    
    for i in range(1,len(Desc)):
        gate = Desc[i][0]
        match gate:
            case 'I' | 'X'  | 'Y' | 'Z' | 'H' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                Liste = Desc[i][1]
                for j in range(len(Liste)):
                    qbno = Liste[j]
                    # Create a Rectangle patch
                    rect = patches.Rectangle((i-0.3, qbno-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                    ax.add_patch(rect)
                    ax.text(i, qbno, gate, fontsize=9, ha='center', va='center')
            
            case 'RTX' | 'RTY' | 'RTZ' :
                Param = Desc[i][1]
                qbno  = Param[0]
                theta = str(Param[1])
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, qbno-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, qbno+0.1, gate, fontsize=9, ha='center', va='center')  # Add the text
                ax.text(i, qbno-0.1, theta[0:3],fontsize=9, ha='center', va='center')  # Add the text
                
            case 'NC' :
                Param = Desc[i][1]
                ctrl  = Param[0]
                qbno  = Param[1]
                
                # Create Link
                poly = np.zeros((2,2), dtype=float)
                poly[0][0] = i
                poly[0][1] = ctrl
                poly[1][0] = i
                poly[1][1] = qbno
                link = patches.Polygon(poly, closed=False, edgecolor='b')
                ax.add_patch(link)
                
                # Create a Circle patch
                circ = patches.Circle((i, ctrl), 0.1, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(circ)
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, qbno-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, qbno+0.1, 'X', fontsize=9, ha='center', va='center')
                
            case 'CX' | 'CY' | 'CZ' |'CS' | 'CT' | 'CH' :
                Param = Desc[i][1]
                ctrl  = Param[0]
                qbno  = Param[1]
                
                # Create Link
                poly = np.zeros((2,2), dtype=float)
                poly[0][0] = i
                poly[0][1] = ctrl
                poly[1][0] = i
                poly[1][1] = qbno
                link = patches.Polygon(poly, closed=False, edgecolor='b')
                ax.add_patch(link)
                
                # Create a Circle patch
                circ = patches.Circle((i, ctrl), 0.1, linewidth=1, edgecolor='k', facecolor='black')
                ax.add_patch(circ)
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, qbno-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, qbno, gate[1:2], fontsize=9, ha='center', va='center')
                
            case 'SW' | 'SWr' | 'SWi' | 'SWir' :
                Param = Desc[i][1]
                q1    = min(Param)
                q2    = max(Param)
                
                # Create Link
                poly = np.zeros((2,2), dtype=float)
                poly[0][0] = i
                poly[0][1] = q1
                poly[1][0] = i
                poly[1][1] = q2
                link = patches.Polygon(poly, closed=False, edgecolor='b')
                ax.add_patch(link)
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, q1-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, q1+0.1, gate[0:2], fontsize=9, ha='center', va='center')
                ax.text(i, q1-0.1, gate[2:4],fontsize=9, ha='center', va='center')
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, q2-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, q2+0.1, gate[0:2], fontsize=9, ha='center', va='center')
                ax.text(i, q2-0.1, gate[2:4],fontsize=9, ha='center', va='center')
                
            case 'XX' | 'XY' | 'YY' | 'ZZ' :
                Param = Desc[i][1]
                q1    = min(Param[0], Param[1])
                q2    = max(Param[0], Param[1])
                theta = str(Param[2])
                
                # Create Link
                poly = np.zeros((2,2), dtype=float)
                poly[0][0] = i
                poly[0][1] = q1
                poly[1][0] = i
                poly[1][1] = q2
                link = patches.Polygon(poly, closed=False, edgecolor='b')
                ax.add_patch(link)
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, q1-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, q1+0.1, gate, fontsize=9, ha='center', va='center')
                ax.text(i, q1-0.1, theta[0:3],fontsize=9, ha='center', va='center')
                
                # Create a Rectangle patch
                rect = patches.Rectangle((i-0.3, q2-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                ax.add_patch(rect)
                ax.text(i, q2+0.1, gate, fontsize=9, ha='center', va='center')
                ax.text(i, q2-0.1, theta[0:3],fontsize=9, ha='center', va='center')
                
            case 'C': 
                CGate  = Desc[i][1]
                Liste = Desc[i][2]
                
                match CGate:
                    case 'X'  | 'Y' | 'Z' | 'H' | 'P' | 'S' | 'T' | 'SRX'  | 'SRY' | 'SRZ' :
                        for j in range (len(Liste)-1):
                            # Create a Circle patch
                            circ = patches.Circle((i, Liste[j]), 0.1, linewidth=1, edgecolor='k', facecolor='black', zorder=2)
                            ax.add_patch(circ)
                        
                        minq = min( Liste[0:len(Liste)-1] )
                        maxq = max( Liste[0:len(Liste)-1] )
                        
                        # Create Link
                        poly = np.zeros((2,2), dtype=float)
                        poly[0][0] = i
                        poly[0][1] = minq
                        poly[1][0] = i
                        poly[1][1] = maxq
                        link = patches.Polygon(poly, closed=False, edgecolor='b')
                        ax.add_patch(link)
                        
                        if (Liste[len(Liste)-1] > maxq):
                            poly = np.zeros((2,2), dtype=float)
                            poly[0][0] = i
                            poly[0][1] = maxq
                            poly[1][0] = i
                            poly[1][1] = Liste[len(Liste)-1]
                            link = patches.Polygon(poly, closed=False, edgecolor='b')
                            ax.add_patch(link)
                        elif (Liste[len(Liste)-1] < minq):
                            poly = np.zeros((2,2), dtype=float)
                            poly[0][0] = i
                            poly[0][1] = minq
                            poly[1][0] = i
                            poly[1][1] = Liste[len(Liste)-1]
                            link = patches.Polygon(poly, closed=False, edgecolor='b')
                            ax.add_patch(link)
                            
                        # Create a Rectangle patch
                        rect = patches.Rectangle((i-0.3, Liste[len(Liste)-1]-0.3), 0.6, 0.6, linewidth=1, edgecolor='k', facecolor='white', zorder=2)
                        ax.add_patch(rect)
                        ax.text(i, Liste[len(Liste)-1], CGate, fontsize=9, ha='center', va='center')
                                
 #                   case 'SW' | 'SWr' | 'SWi' | 'SWir' :
 #                       for j in range (len(Liste)-2):
                            

def Draw_Schmidt(Rank_VN, Entropy_VN, Max_Schmidt_Ranks, Min_Schmidt_Ranks, Max_VN_Entropy, Min_VN_Entropy, ax):

    ax.plot(Max_Schmidt_Ranks, label="Max Schmidt Ranks", linestyle='dashed', color='red')
    ax.plot(Min_Schmidt_Ranks, label="Min Schmidt Ranks", linestyle='dashed', color='brown')
    ax.plot(Rank_VN, label="Schmidt Rank", color='orange')
    ax.plot(Max_VN_Entropy, label="Max Von Neumann Entropy", linestyle='dashed', color='purple')
    ax.plot(Min_VN_Entropy, label="Min Von Neumann Entropy", linestyle='dashed', color='cyan')
    ax.plot(Entropy_VN, label="Von Neumann Entropy", color='blue')

    
    # Get the legend associated with ax
    legend2 = ax.legend()

def OnDoubleClick(event):
    item = tree.selection()[0]
    if len(item) > 8 :
        sysA, sysB = item[9:].split('_')[0], item[9:].split('_')[1]
        #global options_checkbox1, options_checkbox2
        #options_checkbox1, options_checkbox2 = sysA, sysB
        print("SysA :", sysA)
        print("SysB :", sysB)

def Draw_Partitions(root, Phis, fontsize) :
    #from P_Draw_Schmidt import update_plots
    nb_gates = len(Phis)
    global tree
    #global max_schmidt_ranks
    #max_schmidt_ranks = []
    scrollbar = ttk.Scrollbar(root, orient='vertical')
    scrollbar.pack(side='right', fill='y')
    tree = ttk.Treeview(root, selectmode='extended', yscrollcommand = scrollbar.set)
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    tree.tag_configure('fontsize', background='', font=('',fontsize))

    scrollbar.config(command=tree.yview)

    style = ttk.Style()
    style.configure("Treeview.Heading", font = ('', fontsize + int(fontsize/5), 'bold'))

    tree.heading('#0', text='Entanglement relationships between systems partitions')

    for gate in range(nb_gates) :
        state         = Phis[gate]
        vn_partitions = Von_Neumann_Partitions(state)
        max_schmidt   = max(partition[2][0] for partition in vn_partitions)
        #max_schmidt_ranks.append(max_schmidt)
        #print(max_schmidt)
        gate_index    = str(gate)
        gate_id       = 'gate' + str(gate).zfill(3)
        #print("gate item = ", gate_id)
        gate_text     = 'Gate #' + str(gate)
        tree.insert('', gate_index, gate_id, text = gate_text,  tags='fontsize')

        for sr in range(1,max_schmidt+1) :
            sr_index =  gate_index + str(sr)
            sr_id    =  gate_id + '_' + str(sr)
            #print("sr item = ", sr_id)
            sr_text  = 'Schmidt Rank = ' + str(sr)
            count = 0
            for partition in vn_partitions :
                if partition[2][0] == sr :
                    count = count + 1
            if count > 0 :
                tree.insert('', sr_index, sr_id, text = sr_text,  tags='fontsize')
                tree.move(sr_id, gate_id, 'end')

            for partition in vn_partitions :
                if partition[2][0] == sr :
                    sysA, sysB, vn_entropy  = partition[0], partition[1], partition[2][1]
                    partition_index         = sr_index + str(vn_partitions.index(partition))
                    #print(partition_index)
                    partition_id            = sr_id + '_' + str(sysA) + '_' + str(sysB)
                    #print("partition item = ", partition_id)
                    partition_text          = 'Von Neumann entropy = ' + str(vn_entropy) + '\t System A : ' + str(sysA) + '\t System B : ' + str(sysB)
                    #print(partition_index, partition_id, partition_text)
                    tree.insert('', int(partition_index), partition_id, text = partition_text,  tags='fontsize')
                    tree.move(partition_id, sr_id, 'end')
                    #tree.bind("<Double-1>", OnDoubleClick)
    #print(max_schmidt_ranks)