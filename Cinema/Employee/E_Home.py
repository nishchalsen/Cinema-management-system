from tkinter import *
from Employee.E_Movies import AddMovie
from Employee.E_Scheduling import Scheduling
from Customer.UserProfile import User
import os



class Home:
    """Home class: A Employee window.
       - You can go to a different window:
         * Home
         * Movie
         * Scheduling
         * User
         * Sign Out
       - See which branch the employee works at
       - See a Picture of the cinema :)
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
     time
     If window=None create the Tk() object for the first time
     old_window: reference to the tk() object (Login window)
     username: User's username -_-
     location: Location where the employee works. Use to get the database of that location
    """
    def __init__(self, old_window, username, window=None, location=None):
        self.username = username
        self.old_window = old_window

        if window is None:
            self.window = Toplevel()
            self.window.geometry("940x600+300+30")
            self.window.resizable(False, False)
            self.window.protocol("WM_DELETE_WINDOW", self.goto_sign_out)  # Closing the window is same as signing out

            self.window.img1 = PhotoImage(file="image/Background.gif")
            self.background = Label(self.window, image=self.window.img1, width=940, height=600)
            self.background.place(x=0, y=0)
            self.window.theatre = PhotoImage(file="image/theatre.gif")
            self.window.profile_pic = PhotoImage(file="image/Employee.gif")

            # Cinema database path does not change. An employee only works in a single branch
            self.window.location = location
            self.window.cinemaDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{location}.db"))


        else:
            self.window = window
        self.window.title("Home")

        # Storing the class reference inside the self.window object as it is being passed around
        self.window.Home = Home
        self.window.Movie = AddMovie
        self.window.Scheduling = Scheduling
        self.window.User = User

        # Employee Options
        self.home_btn = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5")
        self.home_btn.grid(row=0, column=0, padx=(15, 10))
        self.add_movie_btn = Button(self.window, text=" Movie ", font=("Arial", 30), bd=0, bg="#1F8BF3", command=self.goto_add_movie)
        self.add_movie_btn.grid(row=0, column=1, padx=(0, 10))
        self.cinema_schedule = Button(self.window, text=" Scheduling ", font=("Arial", 30), bd=0, bg="#CA65F5", command=self.goto_cinema_schedule)
        self.cinema_schedule.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7", command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out", font=("Comic Sans", 30), bd=0, bg="#FF916E", command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        self.welcome = Label(self.window, font=("Arial", 20), bd=0)
        self.welcome.grid(row=1, column=0, padx=10, columnspan=6, pady=(20, 0))
        self.welcome.configure(text=f"Welcome {self.username}.")

        self.picture = Label(self.window, image=self.window.theatre, bg="silver", bd=10)
        self.picture.grid(row=2, column=0, columnspan=100, padx=30, pady=20)

        self.location_display = LabelFrame(self.window, text="Cinema Branch", bg="#414141", fg="white")
        self.location_display.place(x=591, y=159)
        self.location_lbl = Label(self.location_display, text=f"{self.window.location}", font=("Arial", 15), width=20,
                                  bg="#C9A594", fg="#3F3F3F")
        self.location_lbl.grid()

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.home_btn, self.add_movie_btn, self.cinema_schedule, self.user, self.sign_out, self.picture,
                        self.welcome, self.location_display, self.location_lbl]

        self.window.mainloop()

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """

        [widget.destroy() for widget in self.widgets]

    def goto_user(self):
        """Takes you to the user window"""

        self.destroy_all()
        self.window.User(username=self.username, window=self.window, old_window=self.old_window, customer=False)

    def goto_add_movie(self):
        """Takes you to the add movie window"""

        self.destroy_all()
        self.window.Movie(username=self.username, window=self.window, old_window=self.old_window)

    def goto_cinema_schedule(self):
        """Takes you to the scheduling window"""

        self.destroy_all()
        self.window.Scheduling(username=self.username, window=self.window, old_window=self.old_window)

    def goto_sign_out(self):
        """Sign out the user and takes you back to the Login menu."""

        self.window.destroy()
        self.old_window.deiconify()


