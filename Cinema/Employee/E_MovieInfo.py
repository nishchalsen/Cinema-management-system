from tkinter import *
from tkinter import scrolledtext
import os

import sqlite3

cinemaDB_path = None


class MovieInfo:
    """MovieInfo class: Movie Info window.
         - Movie Info such as runtime, release date, description and image.
     Location:   It is used to access the database of the cinema branch at that location
     movie_name: movie_name is  required to access that movie's information
     old_window: reference to the tk() object (Previous window)
     """
    def __init__(self, movie_name, location, old_window=None, online_info=False):

        self.movie_name = movie_name

        if location:
            global cinemaDB_path
            cinemaDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{location}.db"))  # DB path

        if online_info:
            self.all_movie_info = online_info
        else:
            self.all_movie_info = self.get_movie_info()

        self.old_window = old_window

        self.window = Toplevel()
        self.window.title(self.movie_name)
        self.window.geometry("690x770+300+10")
        self.window.resizable(False, False)

        # Background
        self.window.bg = PhotoImage(file="image/MovieInfo.gif")
        self.background = Label(self.window, image=self.window.bg, width=690, height=770)
        self.background.grid(row=0, column=0, rowspan=770, columnspan=690)

        self.back = Button(self.window, text="Back", font=("Arial", 15), command=self.go_back)
        self.back.place(x=10, y=10)

        # Title, Image, Runtime, Release date, Description
        self.title = Label(self.window, text=self.movie_name, font=("Arial", 20))
        self.title.grid(row=0, column=0, columnspan=30, pady=10)

        # This checks if the picture exist in the directory
        if os.path.exists(f"./image/Info/{self.movie_name}.gif"):
            self.window.img = PhotoImage(file=f"./image/Info/{self.movie_name}.gif")

        else:
            self.window.img = PhotoImage(file="./image/Error_Info.gif")
        self.image = Label(self.window, image=self.window.img, bg="grey", bd=5)
        self.image.grid(row=1, column=1, padx=60, pady=(0, 5))

        self.runtime = Label(self.window, text=f"Runtime: {self.all_movie_info['runtime']}", font=("Arial", 15))
        self.runtime.grid(row=2, column=1)

        self.release_date = Label(self.window, text=f"Release Date: {self.all_movie_info['release_date']}",
                                  font=("Arial", 15))
        self.release_date.grid(row=3, column=1)

        self.description_title = Label(self.window, text="Description:", font=("Arial", 15))
        self.description_title.grid(row=4, column=1, sticky=W, padx=(53, 0))
        self.description = scrolledtext.ScrolledText(self.window, width=65, height=8, font=("Arial", 12), wrap="word")
        self.description.grid(row=5, column=1, columnspan=10, padx=(15, 0))

        self.description.insert(INSERT, self.all_movie_info["description"])
        self.description.config(state=DISABLED)

    def go_back(self):
        """Close the movie info window (The current window) and go back to the previous window"""
        self.window.destroy()
        self.old_window.deiconify()

    def get_movie_info(self):
        """get_movie_info() ---> return a dictionary which has info on the movie (release date, runtime, description)
        Search the database for the information
        """

        global cinemaDB_path
        db = sqlite3.connect(cinemaDB_path)
        cursor = db.cursor()
        cursor.execute("""SELECT release_date, runtime, description FROM movie WHERE name = ?""", (self.movie_name,))
        info = cursor.fetchone()
        return {"release_date": {info[0]}, "runtime": info[1], "description": info[2]}
