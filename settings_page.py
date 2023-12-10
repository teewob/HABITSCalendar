import tkinter as tk

class SettingsPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.profilePicture = tk.Label(self.frame, image=None) # Add your image here
        self.userName = tk.Label(self.frame, text="") # Add your user's name here
        self.dateOfBirthField = tk.Entry(self.frame)
        self.genderField = tk.Entry(self.frame)
        self.goals = self.getGoals()
        self.completedHabits = self.getCompletedHabits()
        self.archivedHabits = self.getArchivedHabits()

    def getGoals(self):
        # Implement the method to get goals from your database here
        pass

    def getCompletedHabits(self):
        # Implement the method to get completed habits from your database here
        pass

    def getArchivedHabits(self):
        # Implement the method to get archived habits from your database here
        pass