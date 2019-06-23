import sqlite3
from tkinter import *
from tkinter.ttk import Treeview, Combobox
from tkinter import scrolledtext
from tkinter import messagebox
from Employee.E_MovieInfo import MovieInfo
import datetime
from urllib import request, error
import json
import os

cinemaDB_path = None


class AddMovie:
    """AddMovie class: Add Movie window.
        - See your movie list
        - See movie Info
        - Change scheduling status
        - Remove movie
        - Add Movie Manually
        - Use Api to add movies
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
     time
     old_window: reference to the tk() object (Login window)
     If window=None create the Tk() object for the first time
     username: User's username -_-
     """

    def __init__(self, username, window, old_window=None):
        self.state = 1

        self.all_info = None
        self.all_movie_name = None
        self.username = username
        self.old_window = old_window

        self.window = window
        self.window.title("Add Movie")

        global cinemaDB_path
        cinemaDB_path = self.window.cinemaDB_path

        # Employee Options
        self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5", command=self.goto_home)
        self.home.grid(row=0, column=0, padx=(15, 10))
        self.add_movie_btn = Button(self.window, text=" Movie ", font=("Arial", 30), bd=0, bg="#1F8BF3")
        self.add_movie_btn.grid(row=0, column=1, padx=(0, 10))
        self.cinema_schedule = Button(self.window, text=" Scheduling ", font=("Arial", 30), bd=0, bg="#CA65F5",
                                      command=self.goto_cinema_schedule)
        self.cinema_schedule.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7",
                           command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                               command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        self.show_movie_btn = Button(self.window, text="Show Movies", font=("Arial", 20), command=self.show_movie,
                                     bg="#FFBABA", bd=1)
        self.show_movie_btn.place(x=300, y=90)

        self.manually_add_btn = Button(self.window, text="Add Movie", font=("Arial", 20), command=self.manually_add,
                                       bg="#E0E3FF", bd=1)
        self.manually_add_btn.place(x=500, y=90)

        # ------------Show-Movie-----------------------------------------------------------------------------------------------------------------
        # Table and Heading
        self.movie_list_lbl = LabelFrame(self.window, text="Current Movie List", font=("Arial", 15), fg="white",
                                         bg="#414141")
        self.table = Treeview(self.movie_list_lbl)
        self.create_table()
        self.scroll_y = Scrollbar(self.window, orient="vertical", command=self.table.yview)

        # Movie Info
        self.movie_info_btn = Button(self.window, text="Movie Info", font=("Arial", 15), bd=1, command=self.movie_info,
                                     bg="#4B9F7E")

        # Scheduling Status
        self.disable_movie_btn = Button(self.window, text="Change Scheduling Status", font=("Arial", 15), bd=1,
                                        command=self.change_movie_status, bg="#646BAF")
        # Remove Movie
        self.remove_movie_btn = Button(self.window, text="Remove Movie", font=("Arial", 15), bd=1,
                                       command=self.remove_movie, bg="#AF648D")

        # ------Add-Movie-----------------------------------------------------------------------------------------------

        # -- Add movie online ------------------------------------------------------------------------------------------

        # Search online
        self.search_online_lbl = LabelFrame(self.window, text="Search for a movie:", font=("Arial", 15), fg="white", bg="#2ECC71")
        self.search_online_input = Entry(self.search_online_lbl, width=18, font=("Arial", 20))
        self.search_online_input.grid()
        self.search_btn = Button(self.window, text="Search\nMovie", font=("Arial", 15), bd=1,
                                       command=self.search_name, bg="#AED6F1")
        # Movie options
        self.online_movie_lbl = LabelFrame(self.window, text="Choose the movie:", font=("Arial", 15), fg="white", bg="#2ECC71")
        self.online_movie_option = Combobox(self.online_movie_lbl, state="readonly", width=32, font=("Arial", 15))
        # Movie detail
        self.more_detail_btn = Button(self.window, text="Movie Info", font=("Arial", 15), bd=1, bg="#CACFD2",
                                      command=self.more_detail)
        # Add Movie
        self.add_movie_btn = Button(self.window, text="Add Movie", font=("Arial", 15), bd=1, bg="#EDBB99",
                                    command=self.add_online_movie)




        # -- Add Manually ----------------------------------------------------------------------------------------------
        # Movie Name
        self.movie_name_lbl = LabelFrame(self.window, text="Movie Name:", font=("Arial", 15), fg="white", bg="#414141")
        self.movie_name_input = Entry(self.movie_name_lbl, width=15, font=("Arial", 20))

        # Release Date
        self.movie_date_lbl = LabelFrame(self.window, text="Release Date:", font=("Arial", 15), fg="white",
                                         bg="#414141")
        self.movie_date_input = Entry(self.movie_date_lbl, width=10, font=("Arial", 20))
        self.date_format = Label(self.movie_date_lbl, text="Date format (YYYY-MM-DD)", font=("Arial", 13))

        # Run time
        self.movie_runtime_lbl = LabelFrame(self.window, text="Runtime:", font=("Arial", 15), fg="white", bg="#414141")
        self.movie_runtime_input = Entry(self.movie_runtime_lbl, width=10, font=("Arial", 20))
        self.runtime_format = Label(self.movie_runtime_lbl, text="minutes (10-300)", font=("Arial", 13))

        # Description
        self.movie_description_lbl = LabelFrame(self.window, text="Movie Description", font=("Arial", 15), fg="white",
                                                bg="#414141")
        self.description_input = scrolledtext.ScrolledText(self.movie_description_lbl, width=35, height=8,
                                                           font=("Arial", 12), wrap="word")

        # Enter New Movie
        self.enter_btn = Button(self.window, text="Enter Movie", bd=1, font=("Arial", 16), command=self.enter_movie,
                                bg="#AF7D64")

        self.add_movie_widgets = [self.movie_name_lbl, self.movie_name_input, self.movie_date_lbl,
                                  self.movie_date_input, self.date_format, self.movie_runtime_lbl,
                                  self.movie_runtime_input, self.runtime_format, self.movie_description_lbl,
                                  self.description_input, self.enter_btn, self.search_online_lbl, self.search_btn,
                                  self.online_movie_lbl, self.online_movie_option, self.more_detail_btn,
                                  self.add_movie_btn]

        self.widgets = [self.home, self.add_movie_btn, self.cinema_schedule, self.user, self.sign_out,
                        self.show_movie_btn,
                        self.manually_add_btn, self.movie_list_lbl, self.table, self.movie_info_btn,
                        self.disable_movie_btn,
                        self.remove_movie_btn, self.movie_list_lbl, self.table, self.movie_info_btn,
                        self.disable_movie_btn,
                        self.scroll_y, self.remove_movie_btn] + self.add_movie_widgets

        self.show_movie()

    def search_name(self):
        """search_name() -->
        Give the possible movie option
        """
        if not self.search_online_input.get():
            messagebox.showwarning("Invalid", "Please enter first.")
            return None
        self.online_movie_list = get_movie_online(name=self.search_online_input.get())
        if self.online_movie_list:
            self.online_movie_lbl.place(x=550, y=230)
            self.online_movie_option.grid()
            self.online_movie_option["values"] = [i for i in self.online_movie_list.keys()]
            self.online_movie_option.current(0)
            self.more_detail_btn.place(x=550, y=310)
            self.add_movie_btn.place(x=750, y=310)
        else:
            if self.online_movie_list != None:
                messagebox.showwarning("Invalid", "This movie does not exist")
            self.online_movie_lbl.place_forget()
            self.online_movie_option.grid_forget()
            self.more_detail_btn.place_forget()
            self.add_movie_btn.place_forget()

    def more_detail(self):
        """more_detail() --> get the movie info online and send it to the movie info window"""
        movie_id = self.online_movie_list[self.online_movie_option.get()]
        info =get_info_online(movie_id)
        if info:
            name = info["movie_name"]
            self.window.withdraw()
            MovieInfo(movie_name=name, location=False,  online_info=info, old_window=self.window)

    def manually_add(self):
        """manually_add() --> It enables you to add movie manually by your self
        state = 0  means that the window is currently showing show movie.
        Which implies I can change it to manually add movie
        """
        if self.state == 0:
            self.reset()
            self.movie_name_lbl.place(x=100, y=150)
            self.movie_name_input.grid()
            self.movie_name_input.focus()
            self.movie_date_lbl.place(x=100, y=220)
            self.movie_date_input.grid(row=0, column=0)
            self.date_format.grid(row=0, column=1, padx=10)
            self.movie_runtime_lbl.place(x=100, y=290)
            self.movie_runtime_input.grid(row=0, column=0)
            self.runtime_format.grid(row=0, column=1, padx=10)
            self.movie_description_lbl.place(x=100, y=360)
            self.description_input.grid()
            self.enter_btn.place(x=200, y=550)
            self.search_online_lbl.place(x=550, y=150)
            self.search_btn.place(x=850, y=150)

    def show_movie(self):
        """show_movie() --> It enables you to look at the  current movies in the database
        state = 1  means that the window is currently allowing you to manually add movie.
        Which implies I can change it to show movie
        """
        if self.state == 1:
            self.reset()
            self.movie_list_lbl.grid(row=1, column=0, columnspan=5, pady=(110, 15))
            self.table.grid()
            self.create_table(update=True)
            self.movie_info_btn.place(x=180, y=450)
            self.disable_movie_btn.place(x=325, y=450)
            self.remove_movie_btn.place(x=600, y=450)
            self.scroll_y.place(x=771, y=211)

    def reset(self):
        """
        state = 0  means that the window is currently showing show movie.
        state = 1  means that the window is currently allowing you to manually add movie.
        Remove widget in state 1 or state 2
        """
        if self.state == 0:

            self.table.grid_forget()
            self.movie_list_lbl.grid_forget()
            self.movie_info_btn.place_forget()
            self.disable_movie_btn.place_forget()
            self.remove_movie_btn.place_forget()
            self.scroll_y.place_forget()

            self.state = 1
        else:
            [widget.place_forget() for widget in self.add_movie_widgets]
            self.state = 0

    def remove_movie(self):
        """
        remove_movie() --> remove from movie from the database if the condition stated bellow holds
        -If there is no future booking for the movie, then you can remove it from the database
        -If you don't choose any tickets, you will get a message saying "Please choose a movie from the table"
        Technically changing the movie status to deleted rather than removing it permanently from the database
        """
        num = self.table.focus()
        id = self.table.item(num)["values"]
        if id:
            if is_valid_remove(movie_name=id[1]):
                if messagebox.askyesno("Confirm", f"Are you sure you want to delete {id[1]}."):
                    remove_movie(movie_name=id[1])
                    self.create_table(update=True)
            else:
                messagebox.showerror("Invalid",
                                     f"You can not delete this movie because, in the future, there are screenings of {id[1]} taking place.")
        else:
            messagebox.showinfo("Invalid", "Please choose a movie from the table.")

    def change_movie_status(self):
        """change_movie_status() -->
        -Update the movie status to disable if the movie status is enable
        -Update the movie status to enable if the movie status is disable
        -Movie status being disabled means that you can not create a new future
         screening of this movie
        -If you don't choose any tickets, you will get a message saying "Please choose a movie from the table"

       """

        num = self.table.focus()
        id = self.table.item(num)["values"]
        if id:
            if id[4] == "Enabled":
                update_scheduling_status(movie_name=id[1], status="Disabled")
                messagebox.showinfo("Updated",
                                    """Scheduling movie status has been updated. You will not see this movie when scheduling.""")
            else:
                update_scheduling_status(movie_name=id[1], status="Enabled")
                messagebox.showinfo("Updated",
                                    """Scheduling movie status has been updated. You will now see this movie when scheduling.""")
            self.create_table(update=True)
        else:
            messagebox.showinfo("Invalid", "Please choose a movie from the table.")

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]

    def goto_home(self):
        """Takes you to the home window"""

        self.destroy_all()
        self.window.Home(username=self.username, window=self.window, old_window=self.old_window)

    def goto_cinema_schedule(self):
        """Takes you to the scheduling window"""

        self.destroy_all()
        self.window.Scheduling(username=self.username, window=self.window, old_window=self.old_window)

    def goto_user(self):
        """Takes you to the user window"""

        self.destroy_all()
        self.window.User(window=self.window, old_window=self.old_window, username=self.username, customer=False)

    def goto_sign_out(self):
        """Sign out the user and takes you back to the Login menu."""

        self.window.destroy()
        self.old_window.deiconify()

    def enter_movie(self):
        """This is where I validate the movie and if all condtion holds, add the new movie to the database"""

        valid_detail = False
        while not valid_detail:
            # Check the validity of the movie name
            if len(self.movie_name_input.get()) == 0:
                self.movie_name_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Please enter the movie name.")
                self.movie_name_input.config(bg="white")
                break

            if self.movie_name_input.get().lower() in self.all_movie_name:
                self.movie_name_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Movie Already Exists.")
                self.movie_name_input.config(bg="white")
                break

            if not self.movie_date_input.get():
                self.movie_date_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Please enter the date.\nEnter the date in this format:\n(YYYY-MM-DD)")
                self.movie_date_input.config(bg="white")
                break

            # Check the validity of the date
            date = self.movie_date_input.get().split("-")

            if len(date) != 3:
                self.movie_date_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid date.\nWrite the date in this format:\n(YYYY-MM-DD)")
                self.movie_date_input.config(bg="white")
                break
            elif len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
                self.movie_date_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid date.\nWrite the date in this format:\n(YYYY-MM-DD)")
                self.movie_date_input.config(bg="white")

                break
            elif not date[0].isnumeric() or not date[1].isnumeric() or not date[2].isnumeric():
                self.movie_date_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid date.\nWrite the date in this format:\n(YYYY-MM-DD)")
                self.movie_date_input.config(bg="white")

                break
            date = [int(i) for i in date]  # change the date into int
            try:
                date = datetime.datetime(year=date[0], month=date[1], day=date[2])
                logical_start = datetime.datetime(year=1900, month=1, day=1)
                logical_end = datetime.datetime(year=2021, month=1, day=1)
                if date < logical_start:
                    self.movie_date_input.config(bg="#E96A6A")
                    messagebox.showerror("Invalid",
                                         f"Invalid.\nThis movie released in year {date.year}, which is impossible.")
                    self.movie_date_input.config(bg="white")

                    break
                elif date > logical_end:
                    self.movie_date_input.config(bg="#E96A6A")
                    messagebox.showerror("Invalid", f"Invalid\nThis movie is released too far in the future. ")
                    self.movie_date_input.config(bg="white")

                    break

            except ValueError:
                self.movie_date_input.config(bg="#E96A6A")

                messagebox.showerror("Invalid", "Invalid date. This month or date does not exist.")
                self.movie_date_input.config(bg="white")

                break

            # Check the running time
            if not self.movie_runtime_input.get():
                self.movie_runtime_input.config(bg="#E96A6A")

                messagebox.showerror("Invalid", "Please enter the movie running time.")
                self.movie_runtime_input.config(bg="white")

                break
            elif not self.movie_runtime_input.get().isnumeric():
                self.movie_runtime_input.config(bg="#E96A6A")

                messagebox.showerror("Invalid", "Running time is a number.")
                self.movie_runtime_input.config(bg="white")

                break

            time = int(self.movie_runtime_input.get())

            if time < 0:
                self.movie_runtime_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid Movie Running Time.")
                self.movie_runtime_input.config(bg="white")

                break
            elif time < 10:
                self.movie_runtime_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid.\nRunning Time of this movie is too short.")
                self.movie_runtime_input.config(bg="white")

                break
            elif time > 300:
                self.movie_runtime_input.config(bg="#E96A6A")

                messagebox.showerror("Invalid", "Invalid.\nRunning Time of this movie is too long.")
                self.movie_runtime_input.config(bg="white")

                break

            # Check the description
            if len(self.description_input.get(1.0, END)) == 1:
                self.description_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Please enter the description of the movie.")
                self.description_input.config(bg="white")

                break
            elif len(self.description_input.get(1.0, END)) > 2000:
                self.description_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "The movie description to long.")
                self.description_input.config(bg="white")

                break

            valid_detail = True  # While loop statement will be false then it will go to else
        else:
            name = self.movie_name_input.get()
            date = self.movie_date_input.get()
            runtime = self.movie_runtime_input.get()
            description = self.description_input.get(1.0, END)

            self.add_movie_db(name=name, date=date, runtime=runtime, description=description)
            self.create_table(update=True)

    def add_online_movie(self):

        movie_id = self.online_movie_list[self.online_movie_option.get()]
        info = get_info_online(movie_id)
        if info:
            name = info["movie_name"]
            date = info["release_date"]
            runtime = info["runtime"]
            description = info["description"]
            if name in [i[1] for i in self.all_info]:
                messagebox.showwarning("Invalid", "This movie already exists in the database.")
            elif messagebox.askyesno("Question", f"""Are you sure you want to add "{name}" in the database?"""):
                self.add_movie_db(name=name, date=date, runtime=runtime, description=description)
                messagebox.showinfo("Complete", "Movie Added")
        else:
            pass

    def add_movie_db(self, name, date, runtime, description):
        """add_movie_db() --> add the movie inside the database"""
        global cinemaDB_path
        db = sqlite3.connect(cinemaDB_path)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO movie(name, release_date, runtime, description, scheduling_status, deleted)
          VALUES(?,?,?,?,?,?)""", (name, date, runtime, description, "Enabled", "False"))
        messagebox.showinfo("Complete", "Movie added to the database.")
        db.commit()
        db.close()
    def create_table(self, update=False):
        """create_table(update) --> create the table with movie information
             if the argument update=False, then the table is created from scratch
             if the argument update=True, then if will only update the information on the table
             Using method get_movie_info() to get all the movie information
             """

        self.all_info = get_movie_info()
        self.all_movie_name = [info[1].lower() for info in self.all_info]
        # all_info structure:Movie ID Movie Name, Release Date, Runtime
        if not update:
            heading_name = ["Num", "Movie Name", "Release Date", "Runtime", "Scheduling"]

            self.table["show"] = "headings"
            self.table["columns"] = list(range(len(heading_name)))

            for i in range(len(heading_name)):
                self.table.heading(i, text=heading_name[i])

            # I am adjusting the table structure
            self.table.column(0, anchor="center", width=80)
            self.table.column(1, anchor="center", width=200)
            self.table.column(2, anchor="center", width=150)
            self.table.column(3, anchor="center", width=70)
            self.table.column(4, anchor="center", width=100)

            for i in range(len(self.all_info)):
                self.table.insert("", 'end', text="L1", values=(
                    i + 1, self.all_info[i][1], self.all_info[i][2], self.all_info[i][3], self.all_info[i][4]))
        else:
            for i in self.table.get_children():
                self.table.delete(i)
            for i in range(len(self.all_info)):
                self.table.insert("", 'end', text="L1", values=(
                    i + 1, self.all_info[i][1], self.all_info[i][2], self.all_info[i][3], self.all_info[i][4]))

    def movie_info(self):
        """movie_info() --> open the movie info window for that choose movie
        If you don't choose any tickets, you will get a message saying "Please choose a movie from the table"
        """
        num = self.table.focus()
        id = self.table.item(num)["values"]
        if id:
            self.window.withdraw()
            MovieInfo(movie_name=id[1], old_window=self.window, location=self.window.location)
        else:
            messagebox.showinfo("Invalid", "Please choose a movie from the table.")


def get_movie_info():
    """get_movie_info() --> return a list of tuple
    where tuple contains movie info(movie Id, name, release date, runtime, scheduling status)"""
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT movieID, name, release_date, runtime, scheduling_status
                      FROM movie WHERE movie.deleted = "False" """)
    all_info = cursor.fetchall()
    db.close()
    return all_info


def update_scheduling_status(movie_name, status):
    """update_scheduling _status() --> update the movie's scheduling status in the database
    movie_name and status is the two parameter for the function
    movie_name is the movie that is being updated
    status is the movie new scheduling status
    """
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""UPDATE movie SET scheduling_status=? WHERE name=?""", (status, movie_name))
    db.commit()
    db.close()


def is_valid_remove(movie_name):
    """is_valid_remove() --> returns True or False
    Checks if the there is any future screening of the chosen movie taking place
    If yes --> return True, else return False
    """
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT s.date, s.time FROM schedule s, movie m 
                                   WHERE m.movieID = s.movieID AND m.name = ? """, (movie_name,))
    all_info = cursor.fetchall()
    db.close()

    if not all_info:
        return True
    else:

        now = datetime.datetime.now()
        for info in all_info:
            date = info[0]
            time = info[1]

            year, month, day = [int(i) for i in date.split("-")]
            hour, minute = [int(i) for i in time.split(":")]
            screening_datetime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            if screening_datetime >= now:
                return False

        return True


def remove_movie(movie_name):
    """remove_movie(movie_name) --> update the movie's deleted status to "True" and scheduling_status to "Disabled" """
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""UPDATE movie SET deleted="True", scheduling_status="Disabled" WHERE name=?""", (movie_name,))
    messagebox.showinfo("Deleted", f"{movie_name} is deleted.")
    db.commit()
    db.close()


def get_movie_online(name):
    """get_movie_online() --> return list of possible name
    use name to search online
    """
    # Enter the api key to get access to movie database from the website https://www.themoviedb.org/
    key = ""
    
    try:
        with open("themoviedb_api_key.json", "r") as f:
            api_dict = json.load(f)
            key = api_dict["api_key"]
    except FileNotFoundError:
        pass

    try:
        name = name.replace(" ", "%20")
        url = f"https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={name}&page=1&include_adult=false"
        req = request.Request(url=url)
        resp = request.urlopen(req)
        data = json.load(resp)
        name_list = {}
        for i in data["results"]:
            name_list[i["title"]] = i["id"]

        return name_list
    except (error.HTTPError, error.URLError, error.ContentTooShortError):
        messagebox.showwarning("Error", "You can not access this feature at this moment.\nTry again.")
        return None


def get_info_online(movie_id):
    """get_info_online(movie_id) --> returns a dictionary of movie information
    Use the movie_id to search precisely as movie_id are unique
    """
    
    # Getting the API key
    
    try:
        with open("themoviedb_api_key.json", "r") as f:
            json_file = json.load(f)
            key = json_file["api_key"]
    except FileNotFoundError:
        key = ""


    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US"
        req = request.Request(url=url)
        resp = request.urlopen(req)
        data = json.load(resp)

        info = {
            "movie_name": data['original_title'],
            "release_date": data['release_date'],
            "runtime": data['runtime'],
            "description": data['overview']
        }
        return info
    except (error.HTTPError, error.URLError, error.ContentTooShortError):
        messagebox.showwarning("Error", "You can not access this feature at this moment.\nTry again.")
        return False
