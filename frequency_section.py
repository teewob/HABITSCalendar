import tkinter as tk
from tkinter import colorchooser
import json

class FrequencySection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.goalBlock = tk.Label(self.frame, text="Goal Frequency")
        self.goalBlock.pack()

        self.color_box_color = "white"


        # Create a new frame to use grid()
        self.grid_frame = tk.Frame(self.frame)
        self.grid_frame.pack(anchor='center')

        # Initialize row attribute
        self.row = 0

        #dictionary for each frequency
        self.frequencies = {}

        # Dictionary to keep track of the row associated with each frequency frame
        self.frequency_rows = {}

        # Create a frequency
        self.createFrequency()

    def createFrequency(self):
        frequencyFrame = tk.Frame(self.grid_frame, bd=1, relief="solid")
        frequencyFrame.grid(row=self.row, column=0, columnspan=3, sticky='we')
        frequencyFrame.isSelected = False
        frequencyFrame.bind("<Button-1>", self.selectFrequency)

        colorBox = tk.Button(frequencyFrame, bg="white", width=2)
        colorBox.configure(command=lambda button=colorBox: self.choose_color(button))
        colorBox.grid(row=0, column=0)

        rateField = tk.Entry(frequencyFrame, fg='gray')
        rateField.insert(0, "Rate")
        rateField.bind("<Key>", self.updateRateField)
        rateField.grid(row=0, column=1)

        measureField = tk.Entry(frequencyFrame, fg='gray')
        measureField.insert(0, "Measure")
        measureField.bind("<Key>", self.updateMeasureField)
        measureField.grid(row=0, column=2)

        self.frequencies[self.row] = (colorBox, rateField, measureField, frequencyFrame)
        frequencyFrame.row = self.row  # Stores the row number in the frequencyFrame
        self.frequency_rows[
            frequencyFrame] = self.row  # Stores the association between the frequencyFrame and the row in frequency_rows

        self.row += 1

        self.selectedFrequency = frequencyFrame

    # FREQUENCY COLOR BOX
    def choose_color(self, colorBox):
        color = colorchooser.askcolor(title="choose color")
        self.color_box_color = color[1]
        colorBox.configure(bg=self.color_box_color, activebackground=self.color_box_color)
        colorBox.chosen_color = self.color_box_color  # store the chosen color in colorBox


    def updateRateField(self, event):
        event.widget.delete(0, 'end')  # delete placeholder text
        event.widget.config(fg='black')  # change text color to black
        event.widget.unbind("<Key>")  # unbind function from Key event

    def updateMeasureField(self, event):
        event.widget.delete(0, 'end')  # delete placeholder text
        event.widget.config(fg='black')  # change text color to black
        event.widget.unbind("<Key>")  # unbind function from Key event


    #SELECT AND DELETE FREQUENCY
    def selectFrequency(self, event):
        # Deselect the previously selected frequency frame
        if self.selectedFrequency:
            self.selectedFrequency.configure(bg="white")
            self.selectedFrequency.isSelected = False

        # Select the current frequency frame
        frequencyFrame = event.widget
        if self.selectedFrequency == frequencyFrame:
            # If the clicked frequency is already selected, deselect it
            self.selectedFrequency = None
        else:
            # If the clicked frequency is not already selected, select it
            self.selectedFrequency = frequencyFrame
            self.selectedFrequency.configure(bg="light blue")
            self.selectedFrequency.isSelected = True

    def deleteFrequency(self):
        if self.selectedFrequency:  # if a frequency has been selected
            row = self.frequency_rows[
                self.selectedFrequency]  # Get the row associated with the selected frequency frame
            colorBox, rateField, measureField, _ = self.frequencies.pop(row)  # remove the selected frequency
            colorBox.destroy()  # destroy the color box
            rateField.destroy()  # destroy the rate field
            measureField.destroy()  # destroy the measure field
            self.selectedFrequency.destroy()  # destroy the frequency frame

            # Add this line
            del self.frequency_rows[
                self.selectedFrequency]  # Remove the association between the frequency frame and its row

            self.selectedFrequency = None  # reset the selected frequency