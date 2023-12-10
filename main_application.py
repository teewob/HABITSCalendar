import tkinter as tk
from PIL import Image, ImageTk
from tkinter import colorchooser
from home_page import HomePage
from add_habit_page import AddHabitPage
from calendar_page import CalendarPage
from settings_page import SettingsPage
from datetime import datetime
import sqlite3

class MainApplication(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        ...
        self.master.geometry('800x600')  # Set the initial size of the window
        self.master.rowconfigure(999, weight=1)  # 999 is a large number to ensure it's the last row
        self.parent = master
        self.parent.rowconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.homePage = HomePage(parent=self)
        self.addHabitPage = AddHabitPage(parent=self)
        self.calendarPage = CalendarPage(parent=self)
        self.settingsPage = SettingsPage(parent=self)
        self.displayPage(self.homePage)

        self.addHabitPage = AddHabitPage(self)

        #initialize mysql
        self.conn = sqlite3.connect('habits.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS habits
                                  (title text, description text, startDate text, endDate text, frequencies text)''')

        self.navigationIcons = self.createNavigationIcons()

    def saveHabit(self, habit):
        # Insert the habit data into the database
        self.c.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?)",
                       (habit.title, habit.description, habit.start_date, habit.end_date, habit.frequencies))
        self.conn.commit()
#d

    def getHabit(self, title):
        # Query the database for the habit with the given title
        self.c.execute("SELECT * FROM habits WHERE title=?", (title,))
        return self.c.fetchone()


    #getMostRecentHabit method is used to retrieve the most recently inserted habit from the database.
    # It does this by ordering the habits by their row id in descending order and then limiting the results to just 1.
    # The method then returns this habit.
    def getMostRecentHabit(self):
        # Query the database for the most recently inserted habit
        self.c.execute("SELECT * FROM habits ORDER BY rowid DESC LIMIT 1")
        return self.c.fetchone()

    #updateHabit method is used to update an existing habit in the database.
    # It does this by executing an SQL UPDATE statement, which updates the title, description, start date, end date, and frequencies of the habit with the given title.
    def updateHabit(self, habit):
        # Update the habit in the database
        self.c.execute(
            "UPDATE habits SET title = ?, description = ?, startDate = ?, endDate = ?, frequencies = ? WHERE title = ?",
            (habit.title, habit.description, habit.start_date, habit.end_date, habit.frequencies, habit.title))
        self.conn.commit()

    def createNavigationIcons(self):
        navigationFrame = tk.Frame(self)
        navigationFrame.grid(row=0, sticky='n')  # Place navigationFrame in the last row, sticking to the south
        for i in range(5):
            navigationFrame.columnconfigure(i, weight=1)

        homeImage = Image.open(r'C:\Users\Tiara Tenorio\PycharmProjects\HABITSCalendar\icons\home.png')
        homeImage = homeImage.resize((20, 20))  # Resize the image to 20x20 pixels
        self.homeIcon = ImageTk.PhotoImage(homeImage)  # Convert the Image object to a PhotoImage
        homeButton = tk.Button(navigationFrame, image=self.homeIcon, command=lambda: self.displayPage(self.homePage))
        homeButton.grid(row=0, column=0)  # Place the home button at the leftmost position

        # add habit page
        addImage = Image.open(r'C:\Users\Tiara Tenorio\PycharmProjects\HABITSCalendar\icons\add.png')
        addImage = addImage.resize((20, 20))
        self.addIcon = ImageTk.PhotoImage(addImage)
        addButton = tk.Button(navigationFrame, image=self.addIcon, command=lambda: self.displayPage(self.addHabitPage))
        addButton.grid(row=0, column=1)  # Place the add button to the right of the home button

        calendarImage = Image.open(r'C:\Users\Tiara Tenorio\PycharmProjects\HABITSCalendar\icons\calendar.png')
        calendarImage = calendarImage.resize((20, 20))
        self.calendarIcon = ImageTk.PhotoImage(calendarImage)
        calendarButton = tk.Button(navigationFrame, image=self.calendarIcon)
        calendarButton.grid(row=0, column=2)  # Place the calendar button to the right of the add button

        settingsImage = Image.open(r'C:\Users\Tiara Tenorio\PycharmProjects\HABITSCalendar\icons\setting.png')
        settingsImage = settingsImage.resize((20, 20))
        self.settingsIcon = ImageTk.PhotoImage(settingsImage)
        settingsButton = tk.Button(navigationFrame, image=self.settingsIcon)
        settingsButton.grid(row=0, column=3)  # Place the settings button to the right of the calendar button

    def showHomePage(self):
        # Hide all other frames
        self.addHabitPage.frame.grid_remove()
        self.calendarPage.frame.grid_remove()
        self.settingsPage.frame.grid_remove()

        # Show the HomePage
        self.homePage.frame.grid()

    def displayPage(self, page):
        if hasattr(self, 'currentPage'):  # Check if self.currentPage exists
            self.currentPage.frame.grid_remove()  # Remove the current page from the grid
        self.currentPage = page
        self.currentPage.frame.grid()  # Add the new page to the grid