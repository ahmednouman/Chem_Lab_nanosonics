#!/usr/bin/python3

#################################################################
# RASPI MAIN CODE
#
#
# Version: 4.0
# Project: Testing Bench fot Chemical Lab
# Company: Nanosonics
# Author:  Manuel Bernal Lecina
# Date:    7/11/2018
#
#
# Comments:
#   Main class, it runs the GUI itself and controls all the
#   interaction with the board. When executed the pipeline shows
#   a welcome window, then the main Window where a standard file
#   is shown.
#
#   From the Main Window there is access to Loading, Edit, Delete
#   Run, Save, Configuration option, each one represented with
#   an icon.
#
#   The Run Window shows a double table, one for currently
#   and the second one for queued sequences. It has three options
#   PAUSE, STOP and SKIP. Once the last sequence has finished
#   a saving option shows up and the user can choose to save or
#   not.
#
#   The Configuration Window allows the user to change the labels
#   and the configuration of the outputs depending on the
#   hardware that is intended to be connected.
#
#   The Edit Window runs inside the Main Window and allows to
#   add a stage or a loop wherever the user wants by selecting an
#   existing row. Also, there is as Delete button to eliminate a
#   row from the current table.
#
#   The Loading and Save Windows are simple user dialogs. Follow
#   the instructions to achieve the porpoise of each window,
#
#   To exit the program must press Alt+F4
#   
#################################################################


#IMPORTS
import RPi.GPIO as GPIO

import time
import datetime
import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from tkinter import simpledialog
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

from pathlib import Path

#IMPORT CLASSES

from TableClass import Table
#from TestClass import Test
from StageClass import Stage
from RasPiClass import RasPi
from PumpClass import Pump
from DoutClass import Dout
from FlagClass import Flag



#GUI CL

class GUI():
        
    #CONSTANTS
    #-----------------------------------------------------------------------
##    F1W = 1600
##    F1H = 750

    SCREENRATIO = 0.55   #0.46
    VERSION = 'v1.22'


    #CONSTRUCTORS
    #------------------------------------------------------------------------

    #INIT MT
    def __init__(self):
        self.sCount = 0
        self.sequenceCount = 1
        self.runningValues = 0
        self.iterations = 0

        self.data = 0
        
        self.es = []
        self.es1 = []
        self.es2 = []

        self.entries1 = []
        self.entries2 = []
        self.entries3 = []

        self.currentPath = "/home/pi/Desktop/Resources/test_pumps.txt"
        self.currentFolder = "/home/pi/Desktop/Resources/"
        self.currentHz = 100

        self.play2Button = 0
        self.pauseButton = 0
         
        self.currentData = 0
        self.currentConfig = 0
        self.currentLabels = 0
        self.currentValues = 0

        self.getData()

        self.tempConfig = self.currentConfig
        self.tempLabels = self.currentLabels 

        self.nextFlag = Flag()
        self.pauseFlag = Flag()
        self.flag = Flag()
        self.onOff = Flag()

        self.board = RasPi()

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(background='black')

        style = ttk.Style()
        style.theme_use('classic')

        self.F1W = self.root.winfo_screenwidth()*0.99   #0.95
        self.F1H = self.F1W * self.SCREENRATIO

        

        
        try:
            #ICONS and IMGs
            self.Img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/play.png"))
            self.Img2 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/menu.png"))
            self.Img3 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/txt.png"))
            self.Img4 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/stopp.png"))
            self.Img5 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/add.png"))
            self.Img6 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/confirm.png"))
            self.Img7 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/stop.png"))
            self.Img8 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/delete.png"))
            self.Img9 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/save.png"))
            self.Img10 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/next.png"))
            self.Img11 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/pause.png"))
            self.Img12 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/exchange2.png"))
            self.Img13 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/hz.png"))
            self.Img14 = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/Icons/help.png"))
#            welcomeImg = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/Resources/nanosonicscut.png"))
        except:
            messagebox.showwarning("","The resources directory is wrong or non-existent. Please, restore the media files in the following directory and restart the program:  /home/pi/Desktop/Resources")
            self.root.destroy()
        
        
        self.centerW = int(self.getWidth(self.root)/2) 
        self.centerH = int(self.getHeight(self.root)/2)

        fx = self.getX(int(self.getWidth(self.root)),self.F1W)
        fy = self.getY(int(self.getHeight(self.root)), self.F1H)
        self.mainFrame = self.setFrame(self.root, self.F1W, self.F1H, fx, fy)
        

        f3x = self.getX(self.F1W, (self.F1W/2.25))
        f3y = self.getY(self.F1H, (self.F1H/2))
#        self.welcomeFrame = self.setFrame(self.mainFrame, self.F1W/2.25, self.F1H/2, f3x, f3y, 'white')
        
        
#        label1 = tk.Label(self.welcomeFrame, text="Welcome to a Nanosonics Software Solution!")
 #       label1.config(font=('Courier',15), bg='white')
  #      label1.place(relx=0.5, rely=0.2, anchor='c')

#        label2 = tk.Label(self.welcomeFrame, image=welcomeImg)
 #       label2.config(bg='white')
  #      label2.image = welcomeImg
   #     label2.place(relx=0.5, rely=0.5, anchor='c')

        versionLabel = tk.Label(self.root, text=self.VERSION)
        versionLabel.config(font=('Courier',10), bg = 'black', fg='white')
        versionLabel.place(relx=0.50, rely=0.99, anchor='c')

#        self.bContinue = tk.Button(self.welcomeFrame, text=" Continue ", command=self.bContinue)
 #       self.bContinue.config(height=2, width=12, relief='solid', bg='white', font=('Courier',12))
  #      self.bContinue.place(relx=0.5, rely=0.85, anchor='c')

        self.mainFrame.configure(bg='#669966')
        self.root.update()

        self.runTable(self.mainFrame)
        self.root.mainloop()

    #METHODS
    #------------------------------------------------------------------------

    #GENERATE A FRAME IN THE PARAMETERS POSITION AND DIMENSION
    def setFrame(self, parent, w, h, fx, fy, color='black', relieff="flat"):
        frame = tk.Frame(parent, width=w, height=h, relief=relieff, bg=color)
        frame.pack_propagate(0)
        frame.place(x=fx, y=fy)
        return frame

    #GENERATE A FRAME BASED ON THE PARAMETERS relX AND relY
    def relFrame(self, parent, w,h,relx,rely,color='black', relieff="flat"):
        frame = tk.Frame(parent, width=w, height=h, relief=relieff, bg=color)
        frame.pack_propagate(0)
        frame.place(relx=relx, rely=rely, anchor='c')
        return frame

    #GENERATE A LABEL ON A REL POSITION TO THE PARENT PARAMETER
    def relLabel(self, parent, relx, rely, text, size = 30):
        label = tk.Label(parent, text=text, relief='flat', bg=parent.cget('bg'), font=('Courier',size))
        label.text = text
        label.place(relx=relx, rely=rely, anchor='c')
        return label

    def setCurrentPath(self, path):
        self.currentPath = path

    
    #CALCULATE THE VALUE OF THE SCREEN WIDTH AND HEIGHT
    def getWidth(self,parent):
        return parent.winfo_screenwidth()
    def getHeight(self,parent):
        return parent.winfo_screenheight()

    #CALCULATE THE VALUE OF XY TO PRINY IN THE SCREEN
    def getX(self,parw,w):
        return (parw/2) - (w/2)
    def getY(self,parh,h):
        return (parh/2) - (h/2)

    #GENERATE THE MAIN TABLE WITH THE CURRENT STATUS
    def runTable(self, parent):
        self.seqListLabel = self.relLabel(parent,0.5, 0.12, 'Sequence List')
        self.tableFrame = self.relFrame(parent, self.F1W/1.125, self.F1H/2.5, 0.5, 0.4, 'white')
    #    self.currentLabels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
        self.table = Table(self.tableFrame,15, self.currentLabels)
        data = self.currentValues
        i = 0
        for line in data:
            i= (-1)*i+1
            self.sCount += 1
            values = line.split()
            length = len(values)           
                    
            if (length == 15):
                if (i == 1):
                    self.table.LoadTable2Data(self.sCount,values)
                else:
                    self.table.LoadTableData(self.sCount,values) 
            elif (length != 1):
                print("Warning!!--> Error in text file...")
        self.table.setColors()

        #BUTTON 1 play
        
        self.playButton = tk.Button(parent, image=self.Img, command=self.playList)
        self.playButton.place(x=self.F1W-50, y=self.F1H-50, anchor='c')

        #BUTTON 2 config
        
        self.configButton = tk.Button(parent, image=self.Img2, command=self.config)
        self.configButton.place(x=50, y=50, anchor='c')

        #BUTTON 3 load
        
        self.loadButton = tk.Button(parent, image=self.Img3, command=self.loadFile)
        self.loadButton.place(x=120, y=50, anchor='c')

        #BUTTON 4 add
        
        self.addButton = tk.Button(parent, image=self.Img5, command=self.addStage)
        self.addButton.place(x=50, y=self.F1H-50, anchor='c')

        #BUTTON 5 delete
        
        self.delButton = tk.Button(parent, image=self.Img8, command=self.delStage)
        self.delButton.place(x=50, y=self.F1H-120, anchor='c')

        #BUTTON 6 changeLine
        
        #self.changeButton = tk.Button(parent, image=self.Img12, command=self.changeLine)
        #self.changeButton.place(x=50, y=self.F1H-190, anchor='c')                          

        #BUTTON 7 Save

        self.saveButton = tk.Button(parent, image=self.Img9, command=self.askToSave)
        self.saveButton.place(x=190, y=50, anchor='c')

        #BUTTON 8 Hz
        self.hzButton = tk.Button(parent, image=self.Img13, command=self.changeHz)
        self.hzButton.place(x=260, y=50, anchor='c')

        # BUTTON 9 Help
        self.helpButton = tk.Button(parent, image=self.Img14, command=self.help)
        self.helpButton.place(x=self.F1W-50, y=50, anchor='c')
        self.root.update()
        
        self.iterations = self.sCount
        self.sCount = 0

    #GENERATE THE EDIT INPUT WINDOW
    def runEditWin(self, parent):
        self.editFrame = self.relFrame(parent, self.F1W/1.25, self.F1H/4.5, 0.5, 0.85, 'white')
        self.addLabel = self.relLabel(parent,0.5, 0.71, 'Add a Stage or Generate a Loop',14)
        self.editFrameX = self.relFrame(self.editFrame, self.F1W/10, self.F1H/10, 0.07, 0.3, 'white')
        self.editFrame0 = self.relFrame(self.editFrame, self.F1W/10, self.F1H/8, 0.07, 0.74, 'white')
        self.editFrame1 = self.relFrame(self.editFrame, self.F1W/6, self.F1H/6, 0.24, 0.5, 'white')
        self.editFrame2 = self.relFrame(self.editFrame, self.F1W/6, self.F1H/6, 0.44, 0.5, 'white')
        self.editFrame3 = self.relFrame(self.editFrame, self.F1W/6, self.F1H/6, 0.645, 0.5, 'white')
        self.editFrame4 = self.relFrame(self.editFrame, self.F1W/7.5, self.F1H/6, 0.84, 0.6, 'white')
        separator = ttk.Separator(self.editFrame, orient='vertical')
        separator.place(relx=0.74, rely=0.5, relheight=0.9, anchor='c')
        separator2 = ttk.Separator(self.editFrame, orient='vertical')
        separator2.place(relx=0.94, rely=0.5, relheight=0.9, anchor='c')
        separator3 = ttk.Separator(self.editFrame, orient='vertical')
        separator3.place(relx=0.55, rely=0.5, relheight=0.9, anchor='c')
        separator4 = ttk.Separator(self.editFrame, orient='vertical')
        separator4.place(relx=0.14, rely=0.5, relheight=0.9, anchor='c')

        self.editGrids(self.editFrame1, self.entries1, self.currentLabels[4:8])
        self.editGrids(self.editFrame2, self.entries2, self.currentLabels[8:12])
        self.editGrids(self.editFrame3, self.entries3, self.currentLabels[12:16])

        #setup editFrameX
        self.loopLabel = self.relLabel(self.editFrame,0.075, 0.12, 'Label',14)

        self.entryX = tk.Entry(self.editFrameX, width = 11)
        self.entryX.grid(row=0, column=0, padx=4, pady=4)

        #setup editFrame0
        self.loopLabel = self.relLabel(self.editFrame,0.075, 0.5, 'Time',14)

        tk.Label(self.editFrame0, text='Min:', bg=self.editFrame0.cget('bg')).grid(row=0, column=0, padx=4, pady=4)
        self.entry11 = tk.Entry(self.editFrame0, width = 6)
        self.entry11.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(self.editFrame0, text='Sec:', bg=self.editFrame0.cget('bg')).grid(row=1, column=0, padx=4, pady=4)
        self.entry22 = tk.Entry(self.editFrame0, width = 6)
        self.entry22.grid(row=1, column=1, padx=4, pady=4)
        
        #setup editFrame4
        self.enableLoop = tk.IntVar()
        self.check = tk.Checkbutton(self.editFrame, variable=self.enableLoop, command=self.checkBox, bg=self.editFrame.cget('bg'))
        self.check.place(relx=0.815, rely=0.2, anchor='c')

        self.loopLabel = self.relLabel(self.editFrame,0.85, 0.2, 'Loop',14)
        
        tk.Label(self.editFrame4, text='From stage:', bg=self.editFrame4.cget('bg')).grid(row=0, column=0, padx=4, pady=4)
        self.entry1 = tk.Entry(self.editFrame4, width = 8, state='disabled')
        self.entry1.grid(row=0, column=1, padx=4, pady=4)
        
        tk.Label(self.editFrame4, text='To stage:', bg=self.editFrame4.cget('bg')).grid(row=1, column=0, padx=4, pady=4)
        self.entry2 = tk.Entry(self.editFrame4, width = 8, state='disabled')
        self.entry2.grid(row=1, column=1, padx=4, pady=4)

        self.entry3 = tk.Entry(self.editFrame4, width = 10, state='disabled')
        self.entry3.grid(row=2, column=0, padx=4, pady=4)
        tk.Label(self.editFrame4, text='times', bg=self.editFrame4.cget('bg')).grid(row=2, column=1, padx=4, pady=4)

        #BUTTON 1 enter Stage
        self.confirmStageButton = tk.Button(self.editFrame, image=self.Img6, command=self.confirmStage)
        self.confirmStageButton.place(relx=0.97, rely=0.8, anchor='c')

        #BUTTON 2 cancel
        self.cancelStageButton = tk.Button(self.editFrame, image=self.Img7, command=self.cancelStage)
        self.cancelStageButton.place(relx=0.97, rely=0.2, anchor='c')

        #BUTTON 3 change values
        self.exchangeStageButton = tk.Button(self.editFrame, image=self.Img12, command=self.exchangeStage)
        self.exchangeStageButton.place(relx=0.97, rely=0.5, anchor='c')

        self.root.bind('<Double-Button-1>',self.updateValues)

    def updateValues(self, a):
        if self.table.currentValues is not '22':        
            self.entryX.delete('0', 'end')
            self.entryX.insert('0', self.table.currentValues['values'][0])
            self.entry11.delete('0', 'end')
            self.entry11.insert('0', self.table.currentValues['values'][1])
            self.entry22.delete('0', 'end')
            self.entry22.insert('0', self.table.currentValues['values'][2])
            for i in range(4):
                self.entries1[i].delete('0', 'end')
                self.entries1[i].insert('0', self.table.currentValues['values'][3+i])
            for j in range(4):
                self.entries2[j].delete('0', 'end')
                self.entries2[j].insert('0', self.table.currentValues['values'][7+j])
            for k in range(4):
                self.entries3[k].delete('0', 'end')
                self.entries3[k].insert('0', self.table.currentValues['values'][11+k])
                

            
            
    def checkBox(self):
        if(int(self.enableLoop.get()) == 1):
            self.entry1.config(state='normal')
            self.entry2.config(state='normal')
            self.entry3.config(state='normal')
            self.entryX.config(state='disabled')
            self.entry11.config(state='disabled')
            self.entry22.config(state='disabled')
            list(map(lambda x: x.config(state='disabled'), self.entries1))
            list(map(lambda x: x.config(state='disabled'), self.entries2))
            list(map(lambda x: x.config(state='disabled'), self.entries3))
        if(int(self.enableLoop.get()) == 0):
            self.entry1.config(state='disabled')
            self.entry2.config(state='disabled')
            self.entry3.config(state='disabled')
            self.entryX.config(state='normal')
            self.entry11.config(state='normal')
            self.entry22.config(state='normal')
            list(map(lambda x: x.config(state='normal'), self.entries1))
            list(map(lambda x: x.config(state='normal'), self.entries2))
            list(map(lambda x: x.config(state='normal'), self.entries3))
    
    def getNemptyLabels(self, parent, n):
        labels = []
        for i in range(n):
            labels.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
        return labels
    
    def editGrids(self, parent, entries, labels):
        self.emptyLabel = []

                
        if(len(entries)==0):
            for j in range(4):
                entries.append(tk.Entry(parent, width = 10))
                
        if(len(self.emptyLabel)==0):
            self.emptyLabel = self.getNemptyLabels(parent,9)

        tk.Label(parent, text=labels[0], bg=self.editFrame3.cget('bg')).grid(row=0, column=0, padx=4, pady=4)
        self.emptyLabel[0].grid(row=0, column=1, padx=4, pady=4)
        tk.Label(parent, text=labels[1], bg=self.editFrame3.cget('bg')).grid(row=0, column=2, padx=4, pady=4)

        entries[0].grid(row=1, column=0, padx=4, pady=4)
        self.emptyLabel[1].grid(row=1, column=1, padx=4, pady=4)
        entries[1].grid(row=1, column=2, padx=4, pady=4)

        self.emptyLabel[2].grid(row=2, column=0, padx=4, pady=0)
        self.emptyLabel[3].grid(row=2, column=1, padx=4, pady=0)
        self.emptyLabel[4].grid(row=2, column=2, padx=4, pady=0)

        tk.Label(parent, text=labels[2], bg=self.editFrame3.cget('bg')).grid(row=3, column=0, padx=4, pady=4)
        self.emptyLabel[5].grid(row=3, column=1, padx=4, pady=4)
        tk.Label(parent, text=labels[3], bg=self.editFrame3.cget('bg')).grid(row=3, column=2, padx=4, pady=4)

        entries[2].grid(row=4, column=0, padx=4, pady=4)
        self.emptyLabel[6].grid(row=4, column=1, padx=4, pady=4)
        entries[3].grid(row=4, column=2, padx=4, pady=4)


        




    def runConfig(self, parent):
        parent.configure(bg='black')
        self.configFrame = self.relFrame(self.mainFrame, self.F1W/3, self.F1H/1.1, 0.5, 0.5, "#8EC971")
        self.configWindowLabel = self.relLabel(self.configFrame,0.5, 0.08, 'Configuration',20)
        self.pwmLabel = self.relLabel(self.configFrame,0.5, 0.15, 'PWM Outputs',14)
        self.doutLabel = self.relLabel(self.configFrame,0.5, 0.62, 'Digital Outputs',14)
        self.pwmTable = self.relFrame(self.configFrame, self.F1W/5, self.F1H/2.75, 0.5, 0.38, 'white')
        self.doutTable = self.relFrame(self.configFrame, self.F1W/5, self.F1H/2.75, 0.5, 0.76, 'white')
        self.inputGrid(self.pwmTable, "PWM", 3, 8)
        self.inputGrid(self.doutTable, "Dout", 1, 4)
        
        #BUTTON 1 OK
        self.playButton = tk.Button(self.configFrame, text="OK", command=self.closeConfig)
        self.playButton.config(height=1, width=10, relief='solid', bg='white', font=('Courier',10))
        self.playButton.place(relx=0.65, rely=0.93, anchor='c')


        #BUTTON 2 Clear
        self.playButton = tk.Button(self.configFrame, text="Reset", command=self.clearConfig)
        self.playButton.config(height=1, width=10, relief='solid', bg='white', font=('Courier',10))
        self.playButton.place(relx=0.35, rely=0.93, anchor='c')
        self.root.update()

        




    def inputGrid(self, parent, label, nCol, nRows=8):
        
        self.optionsList = ['Simple PWM', "F/B PWMs"]

        if (nCol==1):
            self.emptyLabel = []

            if(len(self.es)==0):
                for j in range(nRows):
                    self.es.append(tk.Entry(parent))
                    
            if(len(self.emptyLabel)==0):
                for j in range(nRows):
                    self.emptyLabel.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
                    self.emptyLabel.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
            
            tk.Label(parent, text=label+'1').grid(row=0, column=0, padx=6, pady=6)
            self.emptyLabel[0].grid(row=0, column=1, padx=6, pady=6)
            tk.Label(parent, text=label+'2').grid(row=0, column=2, padx=6, pady=6)

            self.es[0].grid(row=1, column=0, padx=6, pady=6)
            self.emptyLabel[1].grid(row=1, column=1, padx=6, pady=6)
            self.es[1].grid(row=1, column=2, padx=6, pady=6)

            self.emptyLabel[2].grid(row=2, column=0, padx=6, pady=0)
            self.emptyLabel[3].grid(row=2, column=1, padx=6, pady=0)
            self.emptyLabel[4].grid(row=2, column=2, padx=6, pady=0)

            tk.Label(parent, text=label+'3').grid(row=3, column=0, padx=6, pady=6)
            self.emptyLabel[5].grid(row=3, column=1, padx=6, pady=6)
            tk.Label(parent, text=label+'4').grid(row=3, column=2, padx=6, pady=6)

            self.es[2].grid(row=4, column=0, padx=6, pady=6)
            self.emptyLabel[6].grid(row=4, column=1, padx=6, pady=6)
            self.es[3].grid(row=4, column=2, padx=6, pady=6) 


        if (nCol==3):    
            temp = self.currentConfig
            self.emptyLabels = []
            if(len(self.es1)==0):
                for j in range(int(nRows/2)):
                    self.es1.append(tk.Entry(parent))
                    self.es1.append(tk.Entry(parent))
            if(len(self.emptyLabels)==0):
                for j in range(int(nRows/2)):
                    self.emptyLabels.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
                    self.emptyLabels.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
                    self.emptyLabels.append(tk.Label(parent, text='', relief='flat', bg=parent.cget('bg')))
            if(len(self.es2)==0):
                for j in range(int(nRows/2)):
                    self.es2.append(ttk.Combobox(parent))
                    self.es2[j]['values'] = self.optionsList
                    if(int(temp[j]) == 1):
                        self.es2[j].current(1)
                    else:
                        self.es2[j].current(0)
                    self.es2[j].pos = j

                
            #ROW1
            tk.Label(parent, text=label+'1&2').grid(row=0, column=0, padx=6, pady=6)
            self.emptyLabels[0].grid(row=0, column=1, padx=6, pady=6)
            tk.Label(parent, text=label+'3&4').grid(row=0, column=2, padx=6, pady=6)
            #ROW2
            self.es2[0].grid(row=1, column=0, padx=6, pady=6)
            self.emptyLabels[1].grid(row=1, column=1, padx=6, pady=6)
            self.es2[1].grid(row=1, column=2, padx=6, pady=6)
            self.es2[0].bind("<<ComboboxSelected>>", self.callback)
            self.es2[1].bind("<<ComboboxSelected>>", self.callback)
            #ROW3
            self.es1[0].grid(row=3, column=0, padx=6, pady=6)
            self.emptyLabels[2].grid(row=3, column=1, padx=6, pady=6)
            self.es1[2].grid(row=3, column=2, padx=6, pady=6)         
            #ROW4
            self.es1[1].grid(row=4, column=0, padx=6, pady=6)
            self.emptyLabels[3].grid(row=4, column=1, padx=6, pady=6)
            self.es1[3].grid(row=4, column=2, padx=6, pady=6)
            #ROW5
            self.emptyLabels[5].grid(row=5, column=0, padx=6, pady=0)
            self.emptyLabels[6].grid(row=5, column=1, padx=6, pady=0)
            self.emptyLabels[7].grid(row=5, column=2, padx=6, pady=0)
            #ROW6
            tk.Label(parent, text=label+'5&6').grid(row=6, column=0, padx=6, pady=6)
            self.emptyLabels[8].grid(row=6, column=1, padx=6, pady=6)
            tk.Label(parent, text=label+'7&8').grid(row=6, column=2, padx=6, pady=6)
            #ROW7
            self.es2[2].grid(row=7, column=0, padx=6, pady=6)
            self.emptyLabels[9].grid(row=7, column=1, padx=6, pady=6)
            self.es2[3].grid(row=7, column=2, padx=6, pady=6)
            self.es2[2].bind("<<ComboboxSelected>>", self.callback)
            self.es2[3].bind("<<ComboboxSelected>>", self.callback)
            #ROW8
            self.es1[4].grid(row=8, column=0, padx=6, pady=6)
            self.emptyLabels[10].grid(row=8, column=1, padx=6, pady=6)
            self.es1[6].grid(row=8, column=2, padx=6, pady=6)         
            #ROW9
            self.es1[5].grid(row=9, column=0, padx=6, pady=6)
            self.emptyLabels[11].grid(row=9, column=1, padx=6, pady=6)
            self.es1[7].grid(row=9, column=2, padx=6, pady=6)

            for i in range(4):
                if(int(temp[i]) == 1):
                    self.es1[2*i+1].config(state='disabled')
                else:
                    self.es1[2*i+1].config(state='normal')

              



                

    def callback(self, eventObject):
        if(str(eventObject.widget.get())=="F/B PWM"):
            self.es1[2*int(eventObject.widget.pos)+1].config(state='disabled')
            self.tempConfig[int(eventObject.widget.pos)] = 1
        else:
            self.es1[2*int(eventObject.widget.pos)+1].config(state='normal')
            self.tempConfig[int(eventObject.widget.pos)] = 0

    #GENERATE THE
    def addTimer(self, parent):
        self.minRunningLabel = self.relLabel(parent,0.4, 0.3, 'Countdown: Mins',20)
        self.minFrame = self.relFrame(parent, 60, 35, 0.505, 0.3, 'white')
        self.secRunningLabel = self.relLabel(parent,0.55, 0.3, 'Secs',20)
        self.secFrame = self.relFrame(parent, 40, 35, 0.59, 0.3, 'white')
        self.minLabel = self.relLabel(self.minFrame,0.5, 0.5, '',20)
        self.secLabel = self.relLabel(self.secFrame,0.5, 0.5, '',20)
        
        
    #GENERATE THE MAIN PLAY SETUP
    def runList(self, parent):
        self.seqRunningLabel = self.relLabel(parent,0.5, 0.12, 'Running Sequence')
        self.runningFrame = self.relFrame(parent, self.F1W/1.125, self.F1H/10, 0.5, 0.19, 'white')
        self.seqQueuLabel = self.relLabel(parent,0.5, 0.41, 'Queue Sequences')
        self.queuFrame = self.relFrame(parent, self.F1W/1.125, self.F1H/2.5, 0.5, 0.65, 'white')
        table1 = Table(self.runningFrame,1, self.currentLabels)
        table2 = Table(self.queuFrame,13, self.currentLabels)
        data = self.currentValues
        i = 0
        j = 0
        for line in data:
            self.sCount += 1
            if (self.sequenceCount <= self.sCount):
                i = (-1)*i+1
                j += 1
                values = line.split()
                length = len(values)                  
                if (length == 15):
                    if (j == 1):
                        table1.LoadTable2Data('Running '+str(self.sCount),values)
                        self.runningValues = values
                    else:
                        if (i == 1):
                            table2.LoadTable2Data(str(self.sCount),values)
                        else:
                            table2.LoadTableData(str(self.sCount),values) 
                elif (length != 1):
                    print("Warning!!--> Error in text file...")
        table2.setColors()
        self.sCount = 0

        self.sequenceCount += 1
        
    def disableMainButtons(self):
        self.playButton.config(state='disable')
        self.configButton.config(state='disable')
        self.loadButton.config(state='disable')
        self.addButton.config(state='disable')
        self.saveButton.config(state='disable')
        self.helpButton.config(state='disable')
        self.hzButton.config(state='disable')

    def enableMainButtons(self):
        self.playButton.config(state='normal')
        self.configButton.config(state='normal')
        self.loadButton.config(state='normal')
        self.addButton.config(state='normal')
        self.delButton.config(state='normal')
        self.helpButton.config(state='normal')
        self.saveButton.config(state='normal')
        self.hzButton.config(state='normal')

    def destroyFrames(self):
        self.minLabel.destroy()
        self.secLabel.destroy()
        self.secRunningLabel.destroy()
        self.minRunningLabel.destroy()
        self.seqRunningLabel.destroy()
        self.seqQueuLabel.destroy()
        if not (self.pauseButton == 0):
            self.pauseButton.destroy()
        self.nextButton.destroy()
        if not(self.play2Button == 0):
            self.play2Button.destroy()
        self.stopButton.destroy()
        self.secFrame.destroy()
        self.minFrame.destroy()
        self.runningFrame.destroy()
        self.queuFrame.destroy()
        self.root.update()        

    def destroyFrames2(self):
        self.seqListLabel.destroy()
        self.hzButton.destroy()
        self.saveButton.destroy()
        self.delButton.destroy()
        self.helpButton.destroy()
        self.playButton.destroy()
        self.configButton.destroy()
        self.loadButton.destroy()
        self.addButton.destroy()
        self.tableFrame.destroy()
        self.root.update()
        
    def destroyFrames3(self):
        #list(map(lambda x: x.destroy(), self.es))
        #list(map(lambda x: x.destroy(), self.es1))
        #list(map(lambda x: x.destroy(), self.es2))
        self.es = []
        self.es1 = []
        self.es2 = []
        self.configWindowLabel.destroy()
        self.pwmLabel.destroy()
        self.doutLabel.destroy()
        self.doutTable.destroy()
        self.pwmTable.destroy()
        self.playButton.destroy()
        self.playButton.destroy()
        self.configFrame.destroy()
        self.root.update()

    def destroyFrames4(self):
        #list(map(lambda x: x.destroy(), self.entries1))
        #list(map(lambda x: x.destroy(), self.entries2))
        #list(map(lambda x: x.destroy(), self.entries3))
        self.entries1 = []
        self.entries2 = []
        self.entries3 = []
        self.addLabel.destroy()
        self.confirmStageButton.destroy()
        self.cancelStageButton.destroy()
        self.exchangeStageButton.destroy()
        self.editFrame.destroy()
        self.root.update()

##    def destroyFrames5(self):
##        self.entries1 = []
##        self.entries2 = []
##        self.entries3 = []
##        self.addLabel2.destroy()
##        self.cancelStageButton2.destroy()
##        self.exchangeStageButton2.destroy()
##        self.editFrame2.destroy()
##        self.root.update()

    def getConfig(self, data):
        self.currentConfig = data[0].split()
        return data[0].split()

    def getLabels(self, data):
        #self.currentLabels = data[1].split()
        self.currentLabels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
    def getValues(self,data):
        self.currentValues = data[2:]

    #GET DATA FROM TXT FILE
    def getData(self):
        #READ TXT FILE TO GET ALL THE STAGES AND GENERATE A LIST OF THEM
        #filePath = Path(self.currentPath)
        #CHECK THE FILE EXISTS
        if (Path(self.currentPath).is_file()):
            f = open(self.currentPath,'r')
            self.data = f.readlines()
            f.close()

        else:
            #BYPASS THE MAIN LOOPS AND RUN INTO THE END PROGRAM SECUENCE
            print("Warning!! --> File not found...")
            self.data.append("22")
            self.power = True

        self.currentData = self.data
        self.getConfig(self.data)
        self.getLabels(self.data)
        self.getValues(self.data)

    def getFinalData(self):
        self.fData = []
        for i in range(len(self.currentConfig)):
            if (i == len(self.currentConfig)-1):
                self.fData.append(''.join(self.currentConfig[i])+'\n')
            else:
                self.fData.append(''.join(self.currentConfig[i])+' ')

        for i in range(len(self.currentLabels)):
            if (i == len(self.currentLabels)-1):
                self.fData.append(''.join(self.currentLabels[i])+'\n')
            else:
                self.fData.append(''.join(self.currentLabels[i])+' ')
                
        for i in range(len(self.currentValues)):
            self.fData.append(''.join(self.currentValues[i]))
        return self.fData
        

    def generateTxt(self, path, title):
        #print(title)
        file = open(path+"/"+title+".txt", 'w')
        file.writelines(self.getFinalData())
        file.close()
    
        
    def getTimeStamp(self):
        timestamp = datetime.datetime.utcnow().strftime("%d-%m-%Y_%H%M%S")
        print(timestamp)
        return timestamp

    def delay(self,value):
        time.sleep(value)


    #BUTTON METHODS
    #------------------------------------------------------------------------

    def bContinue(self):
        self.welcomeFrame.destroy()
        self.mainFrame.configure(bg='#669966')
        self.root.update()
        self.runTable(self.mainFrame)

    def playList(self):
        self.destroyFrames2()
        self.mainFrame.configure(bg='#666999')
        #self.mainFrame.configure(bg='#E2A821')
        self.root.update()
        #self.board = 0
        self.flag.setValue(True)
        self.nextFlag.setValue(False)
        self.pauseFlag.setValue(False)
        self.onOff.setValue(True)
        while (self.iterations > 1 and self.flag.value):
            try:
                self.runList(self.mainFrame)
                self.addTimer(self.mainFrame)
                self.stopButton = tk.Button(self.mainFrame, image=self.Img4, command=self.stopList)
                self.stopButton.place(x=self.F1W-140, y=self.F1H-70, anchor='c')
                self.pauseButton = tk.Button(self.mainFrame, image=self.Img11, command=self.pauseList)
                self.pauseButton.place(x=self.F1W-210, y=self.F1H-70, anchor='c')
                self.nextButton = tk.Button(self.mainFrame, image=self.Img10, command=self.nextList)
                self.nextButton.place(x=self.F1W-70, y=self.F1H-70, anchor='c')
                self.root.update()
                self.board.setAll(self.runningValues, self.root, self.minLabel, self.secLabel, self.flag, self.pauseFlag, self.nextFlag, self.currentConfig, self.currentHz)

                self.pauseFlag.setValue(False)
                self.nextFlag.setValue(False)

                if(self.onOff.value):
                    #del self.board
                    self.iterations -= 1
                    self.destroyFrames()
                else:
                    self.minRem = self.minLabel.text
                    self.secRem = self.secLabel.text
                    #del self.board

            except Exception as err:
                #HANDLER
                print("Warning!!--> General Error XXXXX")
                print(err.__class__)
                print(err)

        if(self.onOff.value):
            self.iterations = 0
            self.sequenceCount = 1

            self.askToSave()
        
            self.mainFrame.configure(bg='#669966')
            self.runTable(self.mainFrame)
            self.root.update()

    def pauseList(self):
        self.pauseFlag.setValue(True)
        self.pauseButton.destroy()
        self.pauseButton = 0
        self.play2Button = tk.Button(self.mainFrame, image=self.Img, command=self.playList2)
        self.play2Button.place(x=self.F1W-210, y=self.F1H-70, anchor='c')

    def playList2(self):
        self.pauseFlag.setValue(False)
        self.play2Button.destroy()
        self.play2Button = 0
        self.pauseButton = tk.Button(self.mainFrame, image=self.Img11, command=self.pauseList)
        self.pauseButton.place(x=self.F1W-210, y=self.F1H-70, anchor='c')


    def nextList(self):
        self.nextFlag.setValue(True)

    def stopList(self):
        self.flag.setValue(False)
        self.onOff.setValue(False)
        self.nextFlag.setValue(False)
        self.pauseFlag.setValue(False)
        self.destroyFrames()
        self.sequenceCount = 1        
        self.mainFrame.configure(bg='#669966')
        self.runTable(self.mainFrame)
        self.root.update()

        
    def askToSave(self):
        answer = messagebox.askyesno("Save file", "Do you want to generate a file with the configuration and the data from this execution?")
        self.ver = False
        if(answer):
            path = filedialog.askdirectory(initialdir=self.currentFolder, title="Select folder")
            print(path)
            #while self.ver is False:
            if path:                
                #if(answer):
                fileList = ""
                files = os.listdir(path)
                for file in files:
                    if file.endswith('.txt'):
                        if(file != '.txt'):
                            fileList += file
                            fileList += ' \n '
                title = simpledialog.askstring("File Name", " Please, introduce a name for the file. \n If empty, current time stamp would be used. \n\n The list below shows the existing files at the selected directory: \n\n " + fileList)
                if (title == ""):
                    self.ver = self.generateTxt(path, self.getTimeStamp())
                elif (title+".txt") in files:
                    messagebox.showwarning("","This file alreday exist, please introduce a valid name")
                    title = simpledialog.askstring("File Name", " Please, introduce a name for the file. \n If empty, current time stamp would be used. \n\n The list below shows the existing files at the selected directory: \n\n " + fileList)
                else:
                    self.ver = self.generateTxt(path, title)
        
    def changeHz(self):
        hz = simpledialog.askinteger("Change Frequency (Hz)", "Please, introduce a the new Frequency for the PWM outputs\n\nCurrent Frequency is: " + str(self.currentHz) + " Hz")
        if(hz != None and hz > 0):
            self.currentHz = hz
            #self.board.changeHz(self.currentHz)
        

    def config(self):
        self.destroyFrames2()
        self.runConfig(self.mainFrame)
        messagebox.showwarning("","If you change the current Configuration the current values will be delated. \n Save your data before doing this.")
        
    def loadFile(self):
        self.destroyFrames2()
        self.mainFrame.configure(bg='#669966')
        self.root.update()
        self.filePath = filedialog.askopenfilename(initialdir="/home/pi/Desktop/Resources/", title="Select configuration file", filetypes=(("Text Files","*.txt"),))
        if(self.filePath):
            self.setCurrentPath(self.filePath)
        self.getData()
        self.runTable(self.mainFrame)

    def help(self):
        self.destroyFrames2()
    
        messagebox.showwarning("","         Please read file \n Nanosonics_Chemist Lab Software \n      for how to use this software ")
       
        self.root.update()
        #qpdfview /home/pi/Desktop/Software_Manual.pdf
        self.runTable(self.mainFrame)

    def changeLine(self):
        self.disableMainButtons()
        self.root.update()
        self.runEditWin2(self.mainFrame)
        
    def addStage(self):
        self.disableMainButtons()
        self.root.update()
        self.runEditWin(self.mainFrame)
   
    def delStage(self):
        self.destroyFrames2()
        if not (self.table.currentValues == '22'):
            self.currentValues.pop(int(self.table.currentValues['text'])-1)
        self.root.update()
        self.runTable(self.mainFrame)

    def exchangeStage(self):

        if not (self.table.currentValues == '22'):
            self.currentValues.pop(int(self.table.currentValues['text'])-1)
            
        if(int(self.enableLoop.get()) == 0):
            entries = ''
            if(self.entryX.get()!=''):
                entries+=(self.entryX.get()+' ')
            else:
                entries+='--- '

            if(self.entry11.get()!=''):
                entries+=(self.entry11.get()+' ')
            else:
                entries+='0 '

            if(self.entry22.get()!=''):
                entries+=(self.entry22.get()+' ') 
            else:
                entries+='0 '
                   
            for j in range(4):
                if(self.entries1[j].get()!=''):
                    entries+=(self.entries1[j].get()+' ')
                else:
                    entries+='0 '
                    
            for k in range(4):
                if(self.entries2[k].get()!=''):
                    entries+=(self.entries2[k].get()+' ')
                else:
                    entries+='0 '
                    
            for g in range(4):
                if(g==3):
                    if(self.entries3[g].get()!=''):
                        entries+=(self.entries3[g].get()+'\n')
                    else:
                        entries+='0\n'
                    
                else:
                    if(self.entries3[g].get()!=''):
                        entries+=(self.entries3[g].get()+' ')
                    else:
                        entries+='0 '

            if not (self.table.currentValues == '22'):
                self.currentValues.insert(int(self.table.currentValues['text'])-1,entries)
            else:
                messagebox.showwarning("","Please, select the line you want to change") 
        else:
            if(self.entry1.get()!='' and self.entry2.get()!='' and self.entry3.get()!=''):
                newValues = self.currentValues[int(self.entry1.get())-1:int(self.entry2.get())]
                for i in range(int(self.entry3.get())):
                    for j in range(len(newValues)):
                        if not (self.table.currentValues == '22'):
                            self.currentValues.insert(int(self.table.currentValues['text'])+j,newValues[j])
                        else:
                            self.currentValues.insert(-1, newValues[j])

                
        self.destroyFrames4()
        self.destroyFrames2()
        self.runTable(self.mainFrame)    

    def confirmStage(self):
        if(int(self.enableLoop.get()) == 0):
            entries = ''
            if(self.entryX.get()!=''):
                entries+=(self.entryX.get()+' ')
            else:
                entries+='--- '

            if(self.entry11.get()!=''):
                entries+=(self.entry11.get()+' ')
            else:
                entries+='0 '

            if(self.entry22.get()!=''):
                entries+=(self.entry22.get()+' ') 
            else:
                entries+='0 '
                   
            for j in range(4):
                if(self.entries1[j].get()!=''):
                    entries+=(self.entries1[j].get()+' ')
                else:
                    entries+='0 '
                    
            for k in range(4):
                if(self.entries2[k].get()!=''):
                    entries+=(self.entries2[k].get()+' ')
                else:
                    entries+='0 '
                    
            for g in range(4):
                if(g==3):
                    if(self.entries3[g].get()!=''):
                        entries+=(self.entries3[g].get()+'\n')
                    else:
                        entries+='0\n'
                    
                else:
                    if(self.entries3[g].get()!=''):
                        entries+=(self.entries3[g].get()+' ')
                    else:
                        entries+='0 '

            if not (self.table.currentValues == '22'):
                self.currentValues.insert(int(self.table.currentValues['text']),entries)
            else:
                self.currentValues.insert(-1, entries)
        else:
            if(self.entry1.get()!='' and self.entry2.get()!='' and self.entry3.get()!=''):
                newValues = self.currentValues[int(self.entry1.get())-1:int(self.entry2.get())]
                for i in range(int(self.entry3.get())):
                    for j in range(len(newValues)):
                        if not (self.table.currentValues == '22'):
                            self.currentValues.insert(int(self.table.currentValues['text'])+j,newValues[j])
                        else:
                            self.currentValues.insert(-1, newValues[j])

                
        self.destroyFrames4()
        self.destroyFrames2()
        self.runTable(self.mainFrame)

    def cancelStage(self):
        self.destroyFrames4()
        self.destroyFrames2()
        self.runTable(self.mainFrame)

    def closeConfig(self):
        self.currentConfig = self.tempConfig
        entries = []
        for j in range(8):
            entries.append(self.es1[j])
        for k in range(4):
            entries.append(self.es[k])
        
        for i in range(4):
            if(int(self.currentConfig[i]) == 0):
                if(entries[2*i].get() != ''):
                    self.currentLabels[4 + 2*i] = str(2*i+1) + '-' + entries[2*i].get()
                else:
                    self.currentLabels[4 + 2*i] = str(2*i+1) + '-PWM'
                    
                if(entries[2*i+1].get() != ''):
                    self.currentLabels[4 + 2*i+1] = s
                    tr(2*i + 2) + '-' + entries[2*i+1].get()
                else:
                    self.currentLabels[4 + 2*i] = str(2*i+1) + '-PWM'
                    
            else:
                if(entries[2*i].get() != ''):
                    self.currentLabels[4 + 2*i] = str(i+1) + '-' + entries[2*i].get() + '-dir'
                    self.currentLabels[4 + 2*i+1] = str(i+1) + '-' + entries[2*i].get() + '-speed'
                else:
                    self.currentLabels[4 + 2*i] = str(i+1) + '-PWM-dir'
                    self.currentLabels[4 + 2*i+1] = str(i+1) + '-PWM-speed'
                    

        for i in range(4):
            if(entries[8 + i].get() != ''):
                self.currentLabels[12 + i] = str(i + 1) + '-' + entries[8 + i].get()
            else:
                self.currentLabels[12 + i] = str(i + 1) + '-Dout'
        print(entries)
        self.destroyFrames3()
        
        self.mainFrame.configure(bg='#669966')
        self.root.update()
        self.runTable(self.mainFrame)

    def clearConfig(self):
        self.destroyFrames3()
        self.getData()
        self.runConfig(self.mainFrame)



def main():
    try:
#        Test()
        gui = GUI()
    except:
        GPIO.cleanup()
        gui.root.destroy()


if __name__ == "__main__":
    main()
help
