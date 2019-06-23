from tkinter import *
from tkinter.ttk import Combobox
from Customer.C_Seats import ChooseSeats
from Employee.E_MovieInfo import MovieInfo
import logging
import datetime
import os
from tkinter import messagebox




import sqlite3

cinemaDB_path = None  # Will be changed inside the class
cinema_location = ["London", "Canary Wharf", "The O2 Arena", "Waterloo"]


class Booking:
    """Booking class: Booking window.
        - Choose where you want to watch the movie ["London", "Canary Wharf", "The O2 Arena", "Waterloo"]
        - You choose which movie to watch
        - Book seats
        - See the image of the movie
        - See movie info
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
    time
    old_window: reference to the tk() object (Login window)
    username: User's username -_-
    """
    def __init__(self, window, old_window, username):
        self.username = username
        self.old_window = old_window

        self.window = window
        self.window.title("Booking")
        self.window.theatre = PhotoImage(file="image/theatre.gif")

        # Customers Options
        self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5",
                           command=self.goto_home)
        self.home.grid(row=0, column=0, padx=(15, 10))
        self.booking = Button(self.window, text=" Booking ", font=("Arial", 30), bd=0, bg="#CA65F5")
        self.booking.grid(row=0, column=1, padx=(0, 10))
        self.booked = Button(self.window, text=" Booked ", font=("Arial", 30),
                             bd=0, bg="#1F8BF3", command=self.goto_booked)
        self.booked.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7",
                           command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out ", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                               command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        # Choose the location
        global cinema_location

        self.choose_location_display = LabelFrame(self.window, text="Where will you watch it?", bg="#414141",
                                                  fg="white",
                                                  width=100)
        self.choose_location_display.grid(row=1, column=0, pady=(20, 4))
        self.location_option = Combobox(self.choose_location_display, state="readonly")
        self.location_option["values"] = cinema_location
        self.location_option.current(0)
        self.location_option.grid()
        self.enter_location_btn = Button(self.window, text="Enter Location", command=self.enter_location, bd=2,
                                         bg="#CAE4F8")
        self.enter_location_btn.grid(row=3, column=0, pady=7)

        # Choose Movie
        self.choose_movie_display = LabelFrame(self.window, text="Choose movie:", bg="#414141", fg="white", width=100)
        self.movie_option = Combobox(self.choose_movie_display, state="readonly")
        self.enter_movie_btn = Button(self.window, text="Enter Movie", command=self.enter_name, bd=2, bg="#CAE4F8")

        # Choose Date
        self.choose_date_display = LabelFrame(self.window, text="Choose date:", bg="#414141", fg="white")
        self.date_option = Combobox(self.choose_date_display, state="readonly")
        self.enter_date_btn = Button(self.window, text="Enter Date", command=self.enter_date, bg="#CAE4F8")
        # Choose Time
        self.choose_time_display = LabelFrame(self.window, text="Choose time:", bg="#414141", fg="white")
        self.time_option = Combobox(self.choose_time_display, state="readonly")
        self.enter_time_btn = Button(self.window, text="Enter Time", command=self.enter_time, bg="#CAE4F8")
        # Book Seats
        self.book_seats_btn = Button(self.window, text="Book Seats", font=("Arial", 15), command=self.book_seats,
                                     width=10, height=3, bg="#C9A594", fg="#3F3F3F")
        # No Movie available display
        self.no_movie = Label(self.window, text="Sorry, there are no movies playing.\nPlease come back later.",
                              font=("Arial", 30))

        self.movie_pic = Label(self.window, bg="silver", bd=10, image=self.window.theatre)
        self.movie_pic.place(x=105, y=220)

        self.movie_info_btn = Button(self.window, text="Movie Info", font=("Arial", 15), command=self.movie_info)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.home, self.booked, self.booking, self.user, self.sign_out, self.choose_movie_display,
                        self.movie_option, self.enter_movie_btn, self.movie_pic, self.choose_date_display,
                        self.date_option, self.enter_date_btn, self.choose_time_display, self.time_option,
                        self.enter_time_btn, self.book_seats_btn, self.movie_info_btn, self.no_movie,
                        self.location_option,
                        self.choose_location_display, self.enter_location_btn]


    def movie_info(self):
        self.window.withdraw()
        MovieInfo(movie_name=self.movie_option.get(), old_window=self.window, location=self.location_option.get())

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]

    def goto_home(self):
        """Takes you to the Home window"""
        self.destroy_all()
        self.window.Home(window=self.window, old_window=self.old_window, username=self.username)

    def goto_booked(self):
        """Takes you to the Booked window"""
        self.destroy_all()
        self.window.Booked(window=self.window, old_window=self.old_window, username=self.username)

    def goto_user(self):
        """Takes you to the user window"""
        self.destroy_all()
        self.window.User(window=self.window, old_window=self.old_window, username=self.username, customer=True)

    def goto_sign_out(self):
        """Signs out the user and takes the user back to the Login menu. It also logs the date and the time when the
        user signs out"""

        logging.basicConfig(level=logging.INFO, filename="logging.log")
        logging.info(f"Username: {self.username} Sign-out {datetime.datetime.now()}")
        self.window.destroy()
        self.old_window.deiconify()

    def enter_location(self):
        """enter_location() obtains the location where the user want to watch the movie at.
        Get the path to the database for the cinema branch.
        Then gives the user the list of movie available in that cinema at that location
        Change the enter location button to change location
        Disable the location option"""

        self.location_option.configure(state="disabled")
        self.enter_location_btn.configure(text="Change Location", command=self.change_location)
        global cinemaDB_path
        location = self.location_option.get()
        cinemaDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{location}.db"))

        self.movie_name_dict = get_movie_names()  # Obtain the movie name
        
        # If no names
        if len(self.movie_name_dict) == 0:
            messagebox.showwarning("Sorry", "Sorry, there are not any movie playing in this cinema hall.")

        # Checks if there is any movie playing
        if self.movie_name_dict:
            self.choose_movie_display.grid(row=1, column=1, pady=(20, 4))
            self.movie_option["values"] = [name for name in self.movie_name_dict.keys()]
            self.movie_option.current(0)
            self.movie_option.grid()
            self.movie_option.bind("<<ComboboxSelected>>", lambda e: self.movie_pic.configure(
                image=self.window.booking_img[self.movie_option.get()]))
            self.enter_movie_btn.grid(row=3, column=1, pady=7)

            # Getting the images of the movie
            self.window.booking_img = {}
            for name in self.movie_name_dict.keys():
                if os.path.exists(f"./image/Booking/{name}.gif"):
                    img = PhotoImage(file=f"./image/Booking/{name}.gif")
                else:
                    img = PhotoImage(file="./image/Error_Booking.gif")
                self.window.booking_img[name] = img

            self.movie_pic.configure(image=self.window.booking_img[self.movie_option.get()])
            self.movie_info_btn.place(x=713, y=230)

        else:
            # If there is no movie in the database
            self.no_movie.place(x=200, y=250)

    def enter_name(self):
        """enter_name() select the movie and give a list of available time.
        Change the enter movie button to change movie
        Disable the movie option list
        """

        self.movie_option.configure(state="disabled")
        self.enter_movie_btn.configure(text="Change Movie", command=self.change_movie)

        date = get_dates(movie_id=self.movie_name_dict[self.movie_option.get()])
        if date:
            date.sort()
            self.choose_date_display.grid(row=1, column=2, pady=(20, 4))
            self.date_option["values"] = date
            self.date_option.current(0)
            self.date_option.grid()
            self.enter_date_btn.grid(row=3, column=2, pady=7)

    def enter_date(self):
        """enter_data() select the date and give a list of available time.
        Change the enter date button to change date
        Disable the date option list"""

        self.date_option.configure(state="disabled")
        self.enter_date_btn.configure(text="Change Date", command=self.change_date)
        self.choose_time_display.grid(row=1, column=2, pady=(20, 4), columnspan=3)
        time = get_times(movie_id=self.movie_name_dict[self.movie_option.get()], date=self.date_option.get())
        time.sort()
        self.time_option["values"] = time
        self.time_option.current(0)
        self.time_option.grid()
        self.enter_time_btn.grid(row=3, column=3, pady=7)

    def enter_time(self):
        """enter_date() selects the time, then book seats button appear
        Change the enter time to change time
        Disable the time option list"""

        self.time_option.configure(state="disable")
        self.enter_time_btn.configure(text="Change Time", command=self.change_time)
        self.book_seats_btn.grid(row=1, column=4, rowspan=3)

    def change_location(self):
        """change_location() will enable the the location option
        Change the change location to enter location
        Hide the choose movie, date and time option and book seats button"""

        self.location_option.configure(state="readonly")
        self.enter_location_btn.configure(text="Enter Location", command=self.enter_location)
        self.choose_movie_display.grid_remove()
        self.movie_option.grid_remove()
        self.enter_movie_btn.grid_remove()
        self.movie_info_btn.place_forget()
        self.movie_pic.configure(image=self.window.theatre)

        self.change_movie()

    def change_movie(self):
        """change_movie() will enable the the movie option
          Change the change movie to enter movie
          Hide the choose date and time option and book seats button"""

        self.movie_option.configure(state="readonly")
        self.enter_movie_btn.configure(text="Enter Movie", command=self.enter_name)
        self.choose_date_display.grid_remove()
        self.date_option.grid_remove()
        self.enter_date_btn.grid_remove()
        self.change_date()

    def change_date(self):
        """change_date() will enable the the date option
          Change the change date to enter date
          Hide the choose time option and book seats button"""

        self.enter_date_btn.configure(text="Enter Date", command=self.enter_date)
        self.choose_time_display.grid_remove()
        self.time_option.grid_remove()
        self.enter_time_btn.grid_remove()
        self.date_option.configure(state="readonly")
        self.enter_date_btn.configure(state="normal")
        self.change_time()

    def change_time(self):
        """change_time() will enable the the time option
          Change the change time to enter time
          Hide the seats button"""

        self.enter_time_btn.configure(text="Enter Time", command=self.enter_time)
        self.time_option.configure(state="readonly")
        self.book_seats_btn.grid_remove()

    def book_seats(self):
        """Takes the user to booking seats window"""
        global cinemaDB_path
        db = sqlite3.connect(cinemaDB_path)
        cursor = db.cursor()

        cursor.execute(
            f"""SELECT s.scheduleID FROM seating_plan sp, schedule s
            WHERE s.scheduleID = sp.scheduleID AND date= ? AND time= ?""",
            (self.date_option.get(), self.time_option.get()))
        scheduleID = cursor.fetchone()[0]
        db.close()

        self.window.withdraw()
        location = self.location_option.get()
        ChooseSeats(old_window=self.window, username=self.username, scheduleID=scheduleID, location=location)


def get_movie_names():
    """ get_movie_names() ---> returns a list
    Get the available movie list from the database of that cinema branch. Returns the a dictionary where key is the
    movie ID and the value is the movie name"""

    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT name, movieID FROM movie WHERE movieID IN (SELECT DISTINCT movieID FROM schedule)""")
    info = {name[0]: name[1] for name in cursor.fetchall()}
    temp = {v: k for k, v in info.items()}
    db.close()

    name_and_id = {}
    for movie_id in info.values():
        if get_dates(movie_id):
            name_and_id[temp[movie_id]] = movie_id
    return name_and_id


def get_dates(movie_id):
    """ get_date(movie_id) ---> returns a list
    The function takes the movieId (integer) as an argument
    Get the available date list from the database for that movie name. Returns the a dictionary where key is the
    movie ID and the value is the movie name"""

    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT DISTINCT date FROM schedule WHERE movieID = ? """, (movie_id,))
    date_list = [date[0] for date in cursor.fetchall()]
    db.close()

    new_date_list = []
    now = datetime.datetime.now()

    for date in date_list:
        year, month, day = [int(i) for i in date.split("-")]
        if datetime.datetime(year=year, month=month, day=day) >= now:
            if get_times(movie_id=movie_id, date=date):
                new_date_list.append(date)

    return new_date_list


def get_times(movie_id, date):
    """get_times(movie_id, date) ---> return a list
    The function takes the movieId (integer) and movie date (string) as an argument
    Get the available time list from the database for that movie name and that date. Returns the a dictionary where
    key is the movie ID and the value is the movie name"""

    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT time FROM schedule WHERE movieID = ? and date = ? """, (movie_id, date))
    time_list = [time[0] for time in cursor.fetchall()]
    db.close()

    now = datetime.datetime.now()
    year, month, day = [int(i) for i in date.split("-")]

    if year == now.year and month == now.month and day == now.day:
        new_time_list = []
        for time in time_list:
            hour, minute = [int(i) for i in time.split(":")]
            if hour >= now.hour and minute > now.minute:
                new_time_list.append(time)

        return new_time_list
    else:
        return time_list

