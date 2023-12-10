import tkinter as tk
from habit import Habit
from datetime import datetime
from frequency_section import FrequencySection
import json


class AddHabitPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.editing = False

        #create entry fields
        self.titleEntry = tk.Entry(self.frame)
        self.titleEntry.grid(row=0, column=0)

        # Title
        self.titleField = tk.Entry(self.frame, fg='gray')
        self.titleField.insert(0, "Habit Name")
        self.titleField.bind("<Key>", self.updateTitleField)  # bind function to Key event
        self.titleField.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Description
        self.descriptionField = tk.Text(self.frame, fg='gray', height=5)
        self.descriptionField.insert(1.0, "Habit Description")
        self.descriptionField.bind("<Key>", self.updateDescriptionField)  # bind function to Key event
        self.descriptionField.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.frame.rowconfigure(1, weight=1)

        # Start Date
        self.startDateFrame = tk.Frame(self.frame)  # new frame to contain start date label and entry
        self.startDateLabel = tk.Label(self.startDateFrame, text="Start Date")
        self.startDateFrame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        self.startDateField = tk.Entry(self.startDateFrame)
        self.startDateField.insert(0, datetime.now().date())
        self.startDateField.grid(row=2, column=1, sticky='w')
        self.startDateFrame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        self.frame.rowconfigure(2, weight=1)

        # End Date
        self.endDateVar = tk.StringVar(value="noEnd")  # set default value to "noEnd"
        self.endDateVar.trace('w', self.updateEndDateField)

        # No End Radio Button
        self.noEndRadioButton = tk.Radiobutton(self.frame, text="No End", value="noEnd", variable=self.endDateVar)
        self.noEndRadioButton.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
        self.frame.rowconfigure(3, weight=1)

        # End Date Entry Field and Radio Button
        self.endDateFrame = tk.Frame(self.frame)  # new frame to contain end date radio button and entry
        self.endDateRadioButton = tk.Radiobutton(self.endDateFrame, text="End Date", value="endDate",
                                                 variable=self.endDateVar)
        self.endDateRadioButton.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.endDateField = tk.Entry(self.endDateFrame, state='disabled', fg='gray')
        self.endDateField.insert(0, "YYYY-MM-DD")
        self.endDateField.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.endDateFrame.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
        self.frame.rowconfigure(4, weight=1)

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the frequency section
        self.innerFrame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.innerFrame, anchor='nw')
        self.innerFrame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Frequency Section
        self.frequencySection = FrequencySection(self.innerFrame)
        self.frequencySection.frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Buttons Frame
        self.buttonFrame = tk.Frame(self.frame)
        self.buttonFrame.grid(row=6, column=0, sticky='nsew', padx=5, pady=5)

        # Add Frequency Button
        self.addFrequencyButton = tk.Button(self.buttonFrame, text="Add Frequency",
                                            command=self.frequencySection.createFrequency)
        self.addFrequencyButton.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        # Delete Frequency Button
        self.deleteFrequencyButton = tk.Button(self.buttonFrame, text="Delete Frequency",
                                               command=self.frequencySection.deleteFrequency)
        self.deleteFrequencyButton.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        # Pack the canvas and the scrollbar
        self.canvas.grid(row=5, column=0, sticky='nsew', padx=5, pady=5)
        self.scrollbar.grid(row=5, column=1, sticky='ns', padx=5, pady=5)
        self.frame.rowconfigure(5, weight=1)

        # Save Button
        self.saveButton = tk.Button(self.frame, text="Save Habit", command=self.saveHabitClick)
        self.saveButton.grid(row=7, column=0, sticky='se', padx=5, pady=5)

        # Cancel Button
        self.cancelButton = tk.Button(self.frame, text="Cancel", command=self.cancel)
        self.cancelButton.grid(row=7, column=0, sticky='sw', padx=5, pady=5)

    def updateTitleField(self, event):
        self.titleField.delete(0, 'end')  # delete placeholder text
        self.titleField.config(fg='black')  # change text color to black
        self.titleField.unbind("<Key>")  # unbind function from Key event

    def updateDescriptionField(self, event):
        self.descriptionField.delete(1.0, 'end')  # delete placeholder text
        self.descriptionField.config(fg='black')  # change text color to black
        self.descriptionField.unbind("<Key>")  # unbind function from Key event

    def updateEndDateField(self, *args):
        if self.endDateVar.get() == 'endDate':
            self.endDateField.config(state='normal', fg='black')
        else:
            self.endDateField.config(state='disabled', fg='gray')
            self.endDateField.delete(0, 'end')

    def saveHabitClick(self):
        # Check if all necessary data is filled in
        if self.titleField.get() == '' or self.descriptionField.get('1.0', 'end-1c') == '' or len(
                self.frequencySection.frequencies) == 0:
            tk.messagebox.showerror("Error", "Please fill in all fields.")
            return

        frequencies_dict = {}
        for key, value in self.frequencySection.frequencies.items():
            color_box, rate_field, measure_field, _ = value
            color = color_box.cget("bg")
            rate = rate_field.get()
            measure = measure_field.get()
            frequencies_dict[key] = {'color': color, 'rate': rate, 'measure': measure}

        # Create a new Habit object
        habit = Habit(title=self.titleField.get(),
                      description=self.descriptionField.get('1.0', 'end-1c'),
                      start_date=self.startDateField.get(),
                      end_date=self.endDateField.get(),
                      frequencies=json.dumps(frequencies_dict))

        # If an existing habit is being edited, update it.
        # Otherwise, save the new Habit object through MainApplication class
        if self.editing:
            self.parent.updateHabit(habit)
            print("Habit updated!")
        else:
            self.parent.saveHabit(habit)
            print("Habit saved!")

        # Save the new Habit object through MainApplication class
        self.parent.saveHabit(habit)

        # Display the new habit on the home page
        self.parent.homePage.displayHabit(habit)

        # Switch to the home page
        self.parent.showHomePage()

        # Reset the editing state and clear the fields
        self.editing = False
        self.clear_fields()


    def cancel(self):
        # Clear all fields
        self.clearfields()
        self.titleField.delete(0, 'end')
        self.descriptionField.delete('1.0', 'end')

        # Delete all frequencies
        for colorBox, rateField, measureField, frequencyFrame in self.frequencySection.frequencies.values():
            colorBox.destroy()
            rateField.destroy()
            measureField.destroy()
            frequencyFrame.destroy()
        self.frequencySection.frequencies = {}
        self.frequencySection.frequency_rows = {}

        # Navigate back to the home page
        self.parent.displayPage(self.parent.homePage)

    def clear_fields(self):
        # Clear the title and description fields
        self.titleField.delete(0, 'end')
        self.descriptionField.delete('1.0', 'end')

        # Delete all frequencies
        for colorBox, rateField, measureField, frequencyFrame in self.frequencySection.frequencies.values():
            colorBox.destroy()
            rateField.destroy()
            measureField.destroy()
            frequencyFrame.destroy()
        self.frequencySection.frequencies = {}
        self.frequencySection.frequency_rows = {}