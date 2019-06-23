from tkinter import *
import logging
import datetime
from Customer.C_Booked import Booked
from Customer.C_Booking import Booking
from Customer.UserProfile import User



class Home:
    """Home class: A Customer window.
       - You can go to a different window:
         * Home
         * Booking
         * Booked
         * User
         * Sign Out
       - See a Picture of the cinema :)
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
    time
    If window=None create the Tk() object for the first time
    old_window: reference to the tk() object (Login window)
    username: User's username -_-
    """
    def __init__(self, old_window, username, window=None):
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
            self.window.profile_pic = PhotoImage(file="image/Customer.gif")
        else:
            self.window = window
        self.window.title("Home")

        self.window.Home = Home
        self.window.Booked = Booked
        self.window.Booking = Booking
        self.window.User = User

        # Customers Options
        self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5")
        self.home.grid(row=0, column=0, padx=(15, 10))
        self.booking = Button(self.window, text=" Booking ", font=("Arial", 30), bd=0, bg="#CA65F5",
                              command=self.goto_booking)
        self.booking.grid(row=0, column=1, padx=(0, 10))
        self.booked = Button(self.window, text=" Booked ", font=("Arial", 30), bd=0, bg="#1F8BF3", command=self.goto_booked)
        self.booked.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7", command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                               command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        # Welcome title
        self.welcome = Label(self.window, font=("Arial", 20), bd=0)
        self.welcome.grid(row=1, column=0, padx=10, columnspan=6, pady=(20, 0))
        self.welcome.configure(text=f"Hello {self.username}. What movie will you watch?")

        # Picture
        self.picture = Label(self.window, image=self.window.theatre, bg="silver", bd=10)
        self.picture.grid(row=2, column=0, columnspan=100, padx=30, pady=20)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.home, self.booked, self.booking, self.sign_out, self.picture, self.user, self.welcome]

        self.window.mainloop()

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """

        [widget.destroy() for widget in self.widgets]

    def goto_booked(self):
        """Takes you to the Booked window"""
        self.destroy_all()
        self.window.Booked(window=self.window, old_window=self.old_window, username=self.username)

    def goto_booking(self):
        """Takes you to the booking window"""

        self.destroy_all()
        self.window.Booking(window=self.window, old_window=self.old_window, username=self.username)

    def goto_user(self):
        """Takes you to the user window"""

        self.destroy_all()
        self.window.User(window=self.window, old_window=self.old_window, username=self.username, customer=True)

    def goto_sign_out(self):
        """Sign out the user and takes you back to the Login menu. It also logs the date and the time when the user
        signs out"""

        logging.basicConfig(level=logging.INFO, filename="logging.log")
        logging.info(f"Username: {self.username} Sign-out {datetime.datetime.now()}")
        self.window.destroy()
        self.old_window.deiconify()