import tkinter as tk
from datetime import datetime, timedelta


class HomePage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, padx=50, pady=50)
        self.frame.grid(sticky='nsew')

        # Configure column weights.
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(2, weight=1)

        # Create and grid widgets.
        self.yearLabel = tk.Label(self.frame, text=datetime.now().year)
        self.yearLabel.grid(row=0, column=1, sticky='nsew')

        # Define self.weekFrame and place it in the grid
        self.weekFrame = tk.Frame(self.frame)
        self.weekFrame.grid(row=1, column=1, sticky='nsew')
        self.currentWeekDates = self.getCurrentWeekDates()  # Add this line here
        self.createWeekLabels()

        self.todayHabitsLabel = tk.Label(self.frame, text="Today's Habits")
        self.todayHabitsLabel.grid(row=2, column=1, sticky='nsew')

        self.addHabitsLabel = tk.Label(self.frame, text="Click on + to add habits")
        self.addHabitsLabel.grid(row=3, column=1, sticky='nsew')

        self.habitsFrame = tk.Frame(self.frame)
        self.habitsFrame.grid(row=4, column=1, sticky='nsew')
        self.frame.rowconfigure(4, weight=1)

        # Now you can use self.weekFrame in the grid method
        self.weekFrame.grid(row=1, column=1, sticky='nsew')  # Place the week frame below the year label

        # Create week labels
        self.createWeekLabels()

    def getCurrentYear(self):
        # Implement the method to get the current year here
        pass

    def getCurrentWeekDates(self):
        # Find today's date
        now = datetime.now()

        # Find the start of the week (Sunday)
        startOfWeek = now - timedelta(days=now.weekday() + 1)

        # Get the dates for the rest of the week
        weekDates = [startOfWeek + timedelta(days=i) for i in range(7)]

        return weekDates

    def createWeekLabels(self):
        weekDays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
        weekLabels = []
        for i, date in enumerate(self.currentWeekDates):
            dayOfWeek = date.strftime('%w')  # Get the day of the week as a number (0 is Sunday)

            # If the date is today's date, highlight the label
            if date.date() == datetime.now().date():  # If the date is today's date
                label = tk.Label(self.weekFrame, text=f"{weekDays[int(dayOfWeek)]}", bg="yellow")
                dateLabel = tk.Label(self.weekFrame, text=f"{date.day}", bg="yellow")
            else:
                label = tk.Label(self.weekFrame, text=f"{weekDays[int(dayOfWeek)]}")
                dateLabel = tk.Label(self.weekFrame, text=f"{date.day}")

            label.grid(row=0, column=i)  # Place the label in the grid
            dateLabel.grid(row=1, column=i)  # Place the date label under the day label
            weekLabels.append(label)

        return weekLabels


#habit widget button
    def displayHabit(self, habit):
        # Create a button for the habit
        habitButton = tk.Button(self.habitsFrame, text=habit.title, width=30, command=lambda: self.viewHabit(habit))

        # Use grid to place the button
        row = len(self.habitsFrame.grid_slaves())  # This gives the number of widgets in habitsFrame
        habitButton.grid(row=row, column=0, sticky='w')
        # Create the 3-dot menu
        menuButton = tk.Menubutton(self.habitsFrame, text='...')
        menu = tk.Menu(menuButton)
        menuButton.config(menu=menu)

        # For each command, we're passing the habit data to the function
        menu.add_command(label='EDIT HABIT', command=lambda: self.editHabit(habit))
        menu.add_command(label='ARCHIVE HABIT', command=lambda: self.archiveHabit(habit))
        menu.add_command(label='END HABIT', command=lambda: self.endHabit(habit))
        menu.add_command(label='DELETE HABIT', command=lambda: self.deleteHabit(habit))

        menuButton.grid(row=row, column=1, sticky='w')

    def viewHabit(self, habit):
        print(f"Viewing habit: {habit.title}")

    def editHabit(self, habit):
        # Populate the AddHabitPage form with the habit details
        self.parent.addHabitPage.titleField.delete(0, 'end')
        self.parent.addHabitPage.titleField.insert(0, habit.title)
        self.parent.addHabitPage.descriptionField.delete('1.0', 'end')
        self.parent.addHabitPage.descriptionField.insert('1.0', habit.description)
        # Add the rest of the habit details...


        # Set the editing flag to True
        self.parent.addHabitPage.editing = True

        # Switch to the AddHabitPage
        self.parent.displayPage(self.parent.addHabitPage)