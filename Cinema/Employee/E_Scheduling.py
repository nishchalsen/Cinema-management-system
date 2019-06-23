import sqlite3
from tkinter import *
from tkinter.ttk import Combobox, Treeview
import datetime
from tkinter import messagebox, filedialog
from shutil import copyfile

cinemaDB_path = None




class Scheduling:
    """Scheduling class: Scheduling window.
         - View All, New and Old Scheduling
         - Filter by name, date or both
         - Add new screening
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
     time
     old_window: reference to the tk() object (Login window)
     If window=None create the Tk() object for the first time
     username: User's username -_-
     """
    def __init__(self, username, window, old_window=None):

        self.all_info = None
        self.username = username
        self.old_window = old_window

        self.window = window
        self.window.title("Add Movie")

        global cinemaDB_path
        cinemaDB_path = self.window.cinemaDB_path

        self.movie_name_dict = get_all_movie_names()  # Movie Names

        # Employee Options
        self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5", command=self.goto_home)
        self.home.grid(row=0, column=0, padx=(15, 10))
        self.add_movie = Button(self.window, text=" Movie ", font=("Arial", 30), bd=0, bg="#1F8BF3",
                                command=self.goto_add_movie)
        self.add_movie.grid(row=0, column=1, padx=(0, 10))
        self.cinema_schedule = Button(self.window, text=" Scheduling ", font=("Arial", 30), bd=0, bg="#CA65F5")
        self.cinema_schedule.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7",
                           command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                               command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        # Title
        self.title = Label(self.window, text="Screenings", font=("Arial", 20))
        self.title.grid(row=1, column=2, columnspan=1, pady=15, padx=(100, 0))

        # Table
        self.table = Treeview(self.window)
        self.table.grid(row=2, column=0, columnspan=30, padx=(30, 0), pady=(0, 20))
        self.create_table()

        # Info Type
        self.scheduling_type_lbl = LabelFrame(self.window, text="Scheduling type", fg="white", bg="#414141")
        self.scheduling_type_lbl.place(x=110, y=100)
        self.scheduling_option = Combobox(self.scheduling_type_lbl, state="readonly")
        self.scheduling_option["values"] = ["All Scheduling", "New Scheduling", "Old Scheduling"]
        self.scheduling_option.current(0)
        self.scheduling_option.grid()

        self.scheduling_option.bind("<<ComboboxSelected>>", lambda e: self.scheduling_type())

        # Scroll bar for the table
        self.scroll_y = Scrollbar(self.window, orient="vertical", command=self.table.yview)
        self.scroll_y.place(x=854, y=144)

        # Filter Name
        self.filter_movie_lbl = LabelFrame(self.window, text="Movie Name:", fg="white", bg="#414141")
        self.filter_movie_lbl.grid(row=3, column=1)
        self.filter_name_options = Combobox(self.filter_movie_lbl, state="readonly")
        self.filter_name_options["values"] = list(set([name[0] for name in self.all_info]))
        if self.all_info:
            self.filter_name_options.current(0)
        self.filter_name_options.grid()
        self.filter_movie_btn = Button(self.window, text="Search Movie", command=self.filter_name, bg="#D1D1D1")
        self.filter_movie_btn.grid(row=4, column=1)

        # Filter Date
        self.filter_date_lbl = LabelFrame(self.window, text="Screening Date:", fg="white", bg="#414141")
        self.filter_date_lbl.grid(row=3, column=2)
        self.filter_date_options = Combobox(self.filter_date_lbl, state="readonly")
        self.filter_date_options["values"] = list(set([date[1] for date in self.all_info]))
        if self.all_info:
            self.filter_date_options.current(0)
        self.filter_date_options.grid()
        self.filter_date_btn = Button(self.window, text="Search Date", command=self.filter_date, bg="#D1D1D1")
        self.filter_date_btn.grid(row=4, column=2)

        # Filter Name and Date
        self.filter_name_date_btn = Button(self.window, text="Search \nMovie and Date", command=self.filter_name_date,
                                           bg="#FFE3C9")
        self.filter_name_date_btn.place(x=550, y=402)

        # Reset the table
        self.filter_reset_btn = Button(self.window, text="Reset Filter", command=self.reset_filter, bg="#D3ECFF")
        self.filter_reset_btn.place(x=675, y=410)

        # Export data
        self.export_lbl = LabelFrame(self.window, text="Screening Date:", fg="white", bg="#414141")
        self.export_lbl.grid(row=3, column=4)
        self.export_options = Combobox(self.export_lbl, state="readonly")
        self.export_options["values"] = ["All Scheduling", "New Scheduling", "Old Scheduling", "User Log"]
        self.export_options.current(0)
        self.export_options.grid()
        self.export_data_btn = Button(self.window, text="Export Data", bg="#CFB0D9",
                                      command=lambda: export_data(data_type=self.export_options.get()))
        self.export_data_btn.place(x=792, y=445)

        # Button to open "Add Screening" option
        self.add_screening_btn = Button(self.window, text="Press to add\nScreening", height=3, width=10,
                                        font=("Arial", 12), bd=1, command=self.add_screening, bg="#CFB0D9")

        # Choose Movie
        self.choose_movie_lbl = LabelFrame(self.window, text="Choose movie:", fg="white", bg="#414141")
        self.movie_options = Combobox(self.choose_movie_lbl, state="readonly")
        movies = [name for name in self.movie_name_dict.keys()]
        if movies:
            self.movie_options["values"] = movies
            self.movie_options.current(0)
            self.add_screening_btn.grid(row=3, column=0)
            self.enter_movie_btn = Button(self.window, text="Enter Movie", command=self.enter_movie, bg="#D0D0D0")
        else:
            messagebox.showinfo("Invalid", "There are no movies in the database.")
        # Choose the screening date
        self.choose_date_lbl = LabelFrame(self.window, text="Choose Screening Date:", fg="white", bg="#414141")
        self.date_options = Combobox(self.choose_date_lbl, state="disabled")
        self.choose_date_btn = Button(self.window, text="Enter Date", command=self.enter_date, state="disabled",
                                      bg="#D0D0D0")

        # Choose the screening Hall
        self.choose_hall_lbl = LabelFrame(self.window, text="Enter Screening Room:", fg="white", bg="#414141")
        self.hall_options = Combobox(self.choose_hall_lbl, state="disabled")
        self.choose_hall_btn = Button(self.window, text="Choose Hall", command=self.enter_hall, state="disabled",
                                      bg="#D0D0D0")

        # Choose the screening time
        self.choose_time_lbl = LabelFrame(self.window, text="Choose Screening Time:", fg="white", bg="#414141")
        self.time_options = Combobox(self.choose_time_lbl, state="disabled")
        self.choose_time_btn = Button(self.window, text="Enter Time", command=self.enter_time, state="disabled",
                                      bg="#D0D0D0")

        self.widgets = [self.home, self.add_movie, self.cinema_schedule, self.user, self.sign_out, self.title,
                        self.table, self.filter_movie_lbl, self.filter_name_options, self.filter_movie_btn,
                        self.filter_date_lbl, self.filter_date_options, self.filter_date_btn, self.filter_name_date_btn,
                        self.filter_reset_btn, self.add_screening_btn, self.choose_movie_lbl, self.movie_options,
                        self.enter_movie_btn, self.choose_date_lbl, self.date_options, self.choose_date_btn,
                        self.choose_hall_lbl, self.hall_options, self.choose_hall_btn, self.choose_time_lbl,
                        self.time_options, self.choose_time_btn, self.export_data_btn, self.scroll_y,
                        self.scheduling_option, self.scheduling_type_lbl, self.export_lbl, self.export_options,
                        self.export_data_btn]

    def goto_home(self):
        """Takes you to the home window"""

        self.destroy_all()
        self.window.Home(username=self.username, window=self.window, old_window=self.old_window)

    def goto_add_movie(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        self.destroy_all()
        self.window.Movie(username=self.username, window=self.window, old_window=self.old_window)

    def goto_user(self):
        """Takes you to the user window"""

        self.destroy_all()
        self.window.User(window=self.window, old_window=self.old_window, username=self.username, customer=False)

    def goto_sign_out(self):
        """Sign out the user and takes you back to the Login menu."""

        self.window.destroy()
        self.old_window.deiconify()

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]

    def filter_name(self):
        """filter_name() --> Update the table. Filter the name"""
        new_info = [info for info in self.all_info if info[0] == self.filter_name_options.get()]
        if not new_info:
            new_info = [None]
        self.create_table(update=True, new_info=new_info)

    def filter_date(self):
        """filter_date() --> Update the table. Filter the date"""

        new_info = [info for info in self.all_info if info[1] == self.filter_date_options.get()]
        if not new_info:
            new_info = [None]
        self.create_table(update=True, new_info=new_info)

    def filter_name_date(self):
        """filter_name_date() --> Update the table. Filter the name and date"""


        new_info = [info for info in self.all_info if
                    info[0] == self.filter_name_options.get() and info[1] == self.filter_date_options.get()]
        if not new_info:
            new_info = [None]

        self.create_table(update=True, new_info=new_info)

    def reset_filter(self):
        """reset_filter() --> Update the table. Table with no filter"""

        self.create_table(update=True, info_type=self.scheduling_option.get())

    def scheduling_type(self):
        """scheduling_type() --> Update the table. New table can be:
        - "All Scheduling"
        - "New Scheduling"
        - "Old Scheduling"
        """
        self.create_table(update=True, info_type=self.scheduling_option.get())
        new_names = list(set([name[0] for name in self.all_info]))
        new_dates = list(set([date[1] for date in self.all_info]))
        if not new_names:
            new_names.append("")

        if not new_dates:
            new_dates.append("")
        self.filter_name_options["values"] = new_names
        self.filter_name_options.current(0)
        self.filter_date_options["values"] = new_dates
        self.filter_date_options.current(0)

    def create_table(self, update=False, new_info=None, info_type="All Scheduling"):
        """create_table(update) --> create the table of cinema schedule
        if the argument update=False, then the table is created from scratch
        if the argument update=True, then if will only update the information on the table
        Using method get_scheduling_info() to get the user booked information
        info_type, get different scheduling info for the table
        """
        # all_info structure: Movie Name, Date, Time, Hall, "Booked seats, "Available, Total seats
        if not new_info:
            self.all_info = get_scheduling_info(info_type=info_type)

        if not update:
            heading_name = ["Num", "Movie Name", "Date", "Time", "Hall", "Booked seats", "Available seats",
                            "Total seats"]

            self.table["show"] = "headings"
            self.table["columns"] = list(range(len(heading_name)))

            for i in range(len(heading_name)):
                self.table.heading(i, text=heading_name[i])

            # I am adjusting the table structure
            self.table.column(0, anchor="center", width=60)
            self.table.column(1, anchor="center", width=200)
            self.table.column(2, anchor="center", width=100)
            self.table.column(3, anchor="center", width=70)
            self.table.column(4, anchor="center", width=70)
            self.table.column(5, anchor="center", width=80)
            self.table.column(6, anchor="center", width=90)
            self.table.column(7, anchor="center", width=70)

            for i in range(len(self.all_info)):
                self.table.insert("", 'end', text="L1", values=(
                    i + 1, self.all_info[i][0], self.all_info[i][1], self.all_info[i][2], self.all_info[i][3],
                    self.all_info[i][4], self.all_info[i][5], self.all_info[i][6]))
        else:
            for i in self.table.get_children():
                self.table.delete(i)
            if new_info:
                if not len(new_info) == 0 and new_info[0] is not None:
                    for i in range(len(new_info)):
                        self.table.insert("", 'end', text="L1",
                                          values=(i + 1, new_info[i][0], new_info[i][1], new_info[i][2], new_info[i][3],
                                                  new_info[i][4], new_info[i][5], new_info[i][6]))
            else:
                for i in range(len(self.all_info)):
                    self.table.insert("", 'end', text="L1", values=(
                        i + 1, self.all_info[i][0], self.all_info[i][1], self.all_info[i][2], self.all_info[i][3],
                        self.all_info[i][4], self.all_info[i][5], self.all_info[i][6]))

    def add_screening(self):
        """add_screening() --> enable you to add new screening"""
        self.choose_movie_lbl.grid(row=5, column=1, pady=(20, 5))
        self.movie_options.grid()
        self.enter_movie_btn.grid(row=6, column=1)
        # Just moving the button down and change the text and command
        self.add_screening_btn.grid(row=5, column=0)
        self.add_screening_btn.configure(text="Press to\nCancel", command=self.cancel)

    def cancel(self):
        """cancel() --> disable you to add new screening"""
        forget_sub_widget = [self.time_options, self.hall_options, self.date_options, self.choose_date_lbl,
                         self.choose_hall_lbl, self.choose_time_lbl,
                         self.choose_date_btn, self.choose_time_btn, self.choose_hall_btn, self.movie_options,
                         self.choose_movie_lbl, self.enter_movie_btn]
        [widget.grid_forget() for widget in forget_sub_widget]
        self.add_screening_btn.configure(text="Press to add\nScreening", command=self.add_screening)
        self.add_screening_btn.grid(row=3, column=0)  # Moves the button to its default location

    def enter_movie(self):
        """enter_movie() --> enable you to enter the date"""
        self.choose_date_lbl.grid(row=5, column=2, pady=(20, 5))
        self.date_options.grid()
        self.choose_date_btn.grid(row=6, column=2)

        self.date_options.configure(state="readonly")
        self.choose_date_btn.configure(state="normal")
        self.date_options["values"] = get_screening_date()
        self.date_options.current(0)
        self.movie_options.configure(state="disabled")

        # Changing the enter movie button
        self.enter_movie_btn.configure(text="Change Movie", command=self.change_movie)

    def enter_date(self):
        """enter_date() --> enable you to enter the cinema hall"""
        self.choose_hall_lbl.grid(row=5, column=3, pady=(20, 5))
        self.hall_options.grid()
        self.choose_hall_btn.grid(row=6, column=3)

        self.date_options.configure(state="disable")
        self.hall_options.configure(state="readonly")
        self.choose_hall_btn.configure(state="normal")
        self.hall_options["values"] = [hall for hall in get_screening_rooms()]
        self.hall_options.current(0)

        # Changing the enter date button
        self.choose_date_btn.configure(text="Change Date", command=self.change_date)

    def enter_hall(self):
        """enter_hall() --> enable you to enter the time"""
        time_list = get_screening_time(movie_id=self.movie_name_dict[self.movie_options.get()],
                                       hall=self.hall_options.get(), date=self.date_options.get())

        if time_list:
            self.time_options["values"] = time_list
            self.time_options.current(0)
            self.choose_time_lbl.grid(row=5, column=4, pady=(20, 5))
            self.time_options.grid()
            self.choose_time_btn.grid(row=6, column=4)

            self.hall_options.configure(state="disabled")
            self.time_options.configure(state="readonly")
            self.choose_time_btn.configure(state="normal")

            # Changing the enter hall button
            self.choose_hall_btn.configure(text="Change Hall", command=self.change_hall)

        else:
            messagebox.showwarning("Invalid", "There are no available screening times.")

    def enter_time(self):
        """enter_time() --> ask if you are sure. If yes --> create a new screening"""
        id = self.movie_name_dict[self.movie_options.get()]
        date = self.date_options.get()
        hall = self.hall_options.get()
        time = self.time_options.get()

        text = f"Movie: {self.movie_options.get()}\nDate: {date}\nHall: {hall}\nTime: {time}\nPlease confirm?"

        if messagebox.askyesno("New Screening", text):
            new_screening(movie_id=id, date=date, hall=hall, time=time)

            self.cancel()  # remove the add new screening menu

            self.create_table(update=True)  # Updates the table
            self.filter_name_options["values"] = list(set([name[0] for name in self.all_info]))
            self.filter_name_options.current(0)
            self.filter_date_options["values"] = list(set([date[1] for date in self.all_info]))
            self.filter_date_options.current(0)
            self.change_movie()

    def change_movie(self):
        """change_movie() --> enable you to change the movie"""

        self.date_options.grid_forget()
        self.choose_date_lbl.grid_forget()
        self.date_options.grid_forget()
        self.choose_date_btn.grid_forget()

        self.movie_options.configure(state="readonly")
        self.enter_movie_btn.configure(text="Enter Movie", command=self.enter_movie)

        self.change_date()

    def change_date(self):
        """change_date() --> enable you to change the date"""
        self.choose_hall_lbl.grid_forget()
        self.hall_options.grid_forget()
        self.choose_hall_btn.grid_forget()

        self.date_options.configure(state="readonly")
        self.choose_date_btn.configure(text="Choose Date", command=self.enter_date)

        self.change_hall()

    def change_hall(self):
        """change_hall() --> enable you to change the hall"""

        self.choose_time_lbl.grid_forget()
        self.time_options.grid_forget()
        self.choose_time_btn.grid_forget()

        self.hall_options.configure(state="readonly")
        self.choose_hall_btn.configure(text="Choose Hall", command=self.enter_hall)


# --------Functions-----------------------------------------------------------------------------------------------------


def export_data(data_type):
    """export_date(data_type) --> export data depending on the data type (data_type parameter)"""
    if data_type == "User Log":
        location = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Log files", "*.log"),))
        if location:
            copyfile("logging.log", location)
            messagebox.showinfo("Saved", "File saved.")


    else:
        location = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Csv files", "*.csv"),))

        if location:

            information = get_scheduling_info(info_type=data_type, for_export=True)
            with open(f"{location}.csv", "w") as fp:
                print(data_type, file=fp)
                heading = (
                    "Schedule Id", "Movie Name", "Movie Date", "Movie Time", "Cinema Hall", "Booked seats",
                    "Available Seats",
                    "Total Seats")
                print(",".join(heading), file=fp)
                for info in information:
                    print(",".join([str(i) for i in info]), file=fp)

            messagebox.showinfo("Saved", "File saved.")


def get_scheduling_info(info_type, for_export=False):
    """get_scheduling_info(info_type, for_export) --> return list of movie scheduling information
    for_export: return information which is suitable for exporting
    info_type: return information depending on the information type
    """

    global cinemaDB_path

    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    if for_export:
        cursor.execute("""SELECT s.scheduleID, m.name, s.date, s.time, s.cinema_hall, 
          (sp.total_seats - sp.available_seats)  ,sp.available_seats, sp.total_seats 
          FROM schedule s , movie m, seating_plan sp
          WHERE m.movieID = s.movieID AND s.scheduleID = sp.scheduleID""")
        date_index, time_index = 2, 3
    else:
        cursor.execute("""SELECT m.name, s.date, s.time, s.cinema_hall, (sp.total_seats - sp.available_seats),
                          sp.available_seats, sp.total_seats
                          FROM movie m, schedule s , seating_plan sp
                          WHERE m.movieID = s.movieID
                          AND sp.scheduleID = s.scheduleID""")
        date_index, time_index = 1, 2

    all_info = cursor.fetchall()
    if not for_export:
        all_info = sorted(all_info, key=lambda x: (x[date_index], x[time_index]))

    db.close()
    # Sorts in terms of date and then time
    # Current Date and Time
    date_now = str(datetime.datetime.now())[:10]
    time_now = str(datetime.datetime.now())[11:16]

    if info_type == "All Scheduling":

        return all_info
    elif info_type == "New Scheduling":

        new_info = []

        for info in all_info:
            if info[date_index] > date_now:
                new_info.append(info)
            elif info[date_index] == date_now:
                if info[time_index] >= time_now:
                    new_info.append(info)
        return new_info
    else:
        old_info = []

        for info in all_info:
            if info[date_index] < date_now:
                old_info.append(info)
            elif info[date_index] == date_now:
                if info[time_index] < time_now:
                    old_info.append(info)
        return old_info


def new_screening(movie_id, date, hall, time):
    """new_screening() --> create a new screening. Add it into the database
    the parameter movie_id, data, hall and time is added into the database"""
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT total_seats, cinema_layout FROM cinema_hall WHERE hall=?""", (hall,))
    temp = cursor.fetchone()

    total_seats, layout = temp[0], temp[1]
    cursor.execute("""INSERT INTO schedule(movieID, date, time, cinema_hall) VALUES(?,?,?,?)""",
                   (movie_id, date, time, hall))
    # Find the schedule id
    cursor.execute("""SELECT scheduleID FROM schedule WHERE date=? AND time=? AND cinema_hall=?""", (date, time, hall))
    schedule_id = cursor.fetchone()[0]
    cursor.execute("""INSERT INTO seating_plan(scheduleID, cinema_layout,total_seats,available_seats)
    VALUES (?,?,?,?)""", (schedule_id, layout, total_seats, total_seats))

    db.commit()
    db.close()
    messagebox.showinfo("Finished", "Screening Created !")


def get_all_movie_names():
    """get_all_movie_name() --> return dictionary of movies key:movie Id, value: movie name"""
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT name, movieID FROM movie where scheduling_status="Enabled" """)
    name_and_id = {name[0]: name[1] for name in cursor.fetchall()}
    db.close()

    return name_and_id


def get_screening_rooms():
    """get_screening_rooms() --> return list of cinema hall"""

    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT hall FROM cinema_hall """)
    halls = [hall[0] for hall in cursor.fetchall()]
    db.close()

    return halls


def get_screening_date():
    """get_screening_date() --> return list of screening hall"""

    start = datetime.datetime.now().date()
    dates = []
    for day in range(1, 30):
        start += datetime.timedelta(days=1)
        dates.append(start)
    return dates


def get_screening_time(movie_id, hall, date):
    """get_screening_time(movie_id, hall, date) --> return list of available time which depend on the
     parameter (movie_id, hall, date)"""

    # The earliest movie is at 8 and the last one is at 11
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()

    cursor.execute("""SELECT movieID, runtime FROM movie""")
    movie_runtime_dict = {info[0]: int(info[1]) for info in cursor.fetchall()}

    cursor.execute("""SELECT s.movieID, s.time
    FROM schedule s, movie m
    WHERE m.movieID == s.movieID
    AND cinema_hall = ? AND s.date = ?""", (hall, date))

    booking_history = cursor.fetchall()
    db.close()  # Close the database

    available_time_slot = []
    total_booked = len(booking_history) - 1
    date_split = date.split("-")
    if booking_history:
        for i in range(total_booked + 1):
            # We can book anything after 8, So we should find the available time first
            if i == 0:

                temp = booking_history[i][1].split(":")
                start = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                          hour=8)
                end = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                        hour=int(temp[0]), minute=int(temp[1]))

                # subtracting the running time of the new movie from the first booked

                end -= datetime.timedelta(minutes=movie_runtime_dict[movie_id])

                # round up time base 5
                start += datetime.timedelta(minutes=int(5 * round(float(start.minute) / 5)) - start.minute)
                end -= datetime.timedelta(minutes=end.minute - int(5 * round(float(end.minute) / 5)))

                while start <= end:
                    # Add it to the available time slot
                    available_time_slot.append(start.strftime("%H:%M"))
                    start += datetime.timedelta(minutes=5)

            # If there is booking, do this.
            if i != total_booked:

                temp = booking_history[i][1].split(":")

                start = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                          hour=int(temp[0]), minute=int(temp[1]))
                start += datetime.timedelta(minutes=movie_runtime_dict[booking_history[i][0]])
                start += datetime.timedelta(minutes=int(5 * round(float(start.minute) / 5)) - start.minute)

                temp = booking_history[i + 1][1].split(":")  # Booked movies
                end = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                        hour=int(temp[0]), minute=int(temp[1]))

                while start <= end:
                    # Add it to the list
                    available_time_slot.append(start.strftime("%H:%M"))
                    start += datetime.timedelta(minutes=5)

            else:
                temp = booking_history[total_booked][1].split(":")
                start = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                          hour=int(temp[0]), minute=int(temp[1]))
                end = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]),
                                        hour=22)
                # Adding the last movie runtime to the start time
                start += datetime.timedelta(minutes=movie_runtime_dict[int(booking_history[total_booked][0])])
                end -= datetime.timedelta(minutes=movie_runtime_dict[movie_id])

                # round up time base 5
                start += datetime.timedelta(minutes=int(5 * round(float(start.minute) / 5)) - start.minute)
                end -= datetime.timedelta(minutes=end.minute - int(5 * round(float(end.minute) / 5)))
                while start <= end:
                    # Add it to the available time slot
                    available_time_slot.append(start.strftime("%H:%M"))
                    start += datetime.timedelta(minutes=5)

    else:
        end = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]), hour=22)
        end -= datetime.timedelta(minutes=movie_runtime_dict[movie_id])
        end -= datetime.timedelta(minutes=end.minute - int(5 * round(float(end.minute) / 5)))

        start = datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]), hour=8)
        while start <= end:
            # Add it to the available time slot
            available_time_slot.append(start.strftime("%H:%M"))
            start += datetime.timedelta(minutes=5)

    return available_time_slot

