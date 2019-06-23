from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from Customer.C_Seats import remove_seats
from Employee.E_MovieInfo import MovieInfo
import logging
import datetime
import sqlite3
import os


userDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "User.db"))
cinemaDB_path = None
cinema_location = ["London", "Canary Wharf", "The O2 Arena", "Waterloo"]



class Booked:
    """Booked class: A Booked window.
     - Can view your see your booking history
     - Can remove your booking (only future booking)
     - View Movie detail
     - See your tickets information
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
    time
    old_window: reference to the tk() object (Login window)
    username: User's username -_-"""
    def __init__(self, window, old_window, username):
        self.username = username
        self.old_window = old_window

        self.window = window
        self.window.title("Booked")

        # Customers Options
        self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5", command=self.goto_home)
        self.home.grid(row=0, column=0, padx=(15, 10))
        self.booking = Button(self.window, text=" Booking ", font=("Arial", 30), bd=0, bg="#CA65F5",
                              command=self.goto_booking)
        self.booking.grid(row=0, column=1, padx=(0, 10))
        self.booked = Button(self.window, text=" Booked ", font=("Arial", 30), bd=0, bg="#1F8BF3")
        self.booked.grid(row=0, column=2, padx=(0, 10))
        self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7", command=self.goto_user)
        self.user.grid(row=0, column=3, padx=(0, 10))
        self.sign_out = Button(self.window, text=" Sign Out ", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                               command=self.goto_sign_out)
        self.sign_out.grid(row=0, column=4, padx=(0, 10))

        self.heading = Label(self.window, text="Your movie Tickets", font=("Arial", 20))
        self.heading.grid(row=1, column=0, columnspan=20, pady=(30, 15))

        # all_info structure is : name, date, time, hall, tickets, num_tickets
        self.all_info, self.print_info = [None, None]

        # Table of booked tickets
        self.table = Treeview(self.window)
        self.table.grid(row=2, column=0, columnspan=30, padx=(10, 0))
        # Scroll bar for the table
        self.scroll_y = Scrollbar(self.window, orient="vertical", command=self.table.yview)
        self.scroll_y.place(x=860, y=159)

        self.create_table()  # Creates the table

        # Movie Info Button
        self.movie_info_btn = Button(self.window, text="Movie Info", font=("Arial", 18), command=self.movie_info,
                                     bg="#F69898")
        self.movie_info_btn.place(x=150, y=398)
        # Ticket Info Button
        self.ticket_info_btn = Button(self.window, text="Ticket Info", font=("Arial", 18), command=self.ticket_info,
                                      bg="#788EB2")
        self.ticket_info_btn.place(x=360, y=398)

        # Remove tickets
        self.remove_booking_btn = Button(self.window, text="Remove Booking", font=("Arial", 18), bg="#B28078",
                                         command=self.remove_booking)
        self.remove_booking_btn.place(x=550, y=398)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.home, self.booked, self.booking, self.user, self.sign_out, self.heading, self.table,
                        self.scroll_y, self.movie_info_btn, self.ticket_info_btn, self.remove_booking_btn]



    def goto_home(self):
        """Takes you to the Home window"""

        self.destroy_all()
        self.window.Home(window=self.window, old_window=self.old_window, username=self.username)

    def goto_booking(self):
        """Takes you to the booking window"""

        self.destroy_all()
        self.window.Booking(window=self.window, old_window=self.old_window, username=self.username)

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

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """

        [widget.destroy() for widget in self.widgets]

    def remove_booking(self):
        """ remove_booking() ---> remove future booking
        - If the it is an old booking, you can not remove it
        - If you don't choose any tickets, you will get a message saying "Please choose the ticket first"
        - If you remove the tickets, it updates the database.
        - Updates the available seats, the cinema seats layout and remove your booking from the database"""

        num = self.table.focus()
        id = self.table.item(num)["values"]
        if id:
            year, month, day = [int(num) for num in id[2].split("-")]
            hour, min = [int(time) for time in id[3].split(":")]
            booked_date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=min)
            now = datetime.datetime.now()
            if booked_date >= now:
                if messagebox.askyesno("Confirm", f"Are you sure that you want to delete this ticket?"
                f"\n{self.print_info[id[0]]}"):
                    global cinemaDB_path
                    cinemaDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{id[4]}.db"))
                    db = sqlite3.connect(cinemaDB_path)
                    cursor = db.cursor()
                    cursor.execute("""SELECT sp.cinema_layout, c.user_tickets, c.num_tickets, sp.available_seats, sp.seating_planID, c.ID
                    FROM seating_plan sp, customer_tickets c, schedule s
                    WHERE sp.scheduleID = c.scheduleID
                    AND sp.scheduleID = s.scheduleID
                    AND s.date=? AND s.time=? AND s.cinema_hall=? """, (id[2], id[3], self.all_info[id[0] - 1][3]))
                    temp = cursor.fetchone()
                    cinema_layout = temp[0]
                    user_tickets = temp[1]
                    new_available_seats = temp[3] + temp[2]
                    seating_planID = temp[4]
                    unique_customerID = temp[5]

                    # Update the seating plan beacuse there are free seats now
                    updated_layout = remove_seats(list_layout=cinema_layout, user_tickets=user_tickets)

                    # Update the database
                    cursor.execute("""UPDATE seating_plan SET available_seats=?, cinema_layout=? 
                    WHERE seating_planID=?""", (new_available_seats, updated_layout, seating_planID))
                    cursor.execute("""DELETE FROM customer_tickets WHERE ID=?""", (unique_customerID,))
                    db.commit()

                    self.create_table(update=True)  # Updates the table

            else:
                messagebox.showwarning("Invalid", "You can not delete this ticket")

        else:
            messagebox.showinfo("Invalid", "Please choose the ticket first.")

    def ticket_info(self):
        """ticket_info() --> show the message on your tickets
        Movie name, location, date, time, cinema hall, number of seats, adult tickets, child tickets, seat location,
        cost
        If you don't choose any tickets, you will get a message saying "Please choose the ticket first"  """

        num = self.table.focus()
        id = self.table.item(num)["values"]

        if id:
            messagebox.showinfo("Your ticket", self.print_info[id[0]])
        else:
            messagebox.showinfo("Invalid", "Please choose the ticket first.")

    def movie_info(self):
        """
        movie_into() --> take you the movie information page
        If you don't choose any tickets, you will get a message saying "Please choose the ticket first"
        """
        num = self.table.focus()
        id = self.table.item(num)["values"]
        if id:
            self.window.withdraw()
            MovieInfo(movie_name=id[1], old_window=self.window, location=id[4])
        else:
            messagebox.showinfo("Invalid", "Please choose the ticket first.")

    def create_table(self, update=False):
        """create_table(update) --> create the table with the user booked history
        if the argument update=False, then the table is created from scratch
        if the argument update=True, then if will only update the information on the table
        Using method get_booked_tickets() to get the user booked information
        """

        # all_info structure: name, date, time, hall, tickets, num_tickets
        self.all_info, self.print_info = get_booked_tickets(username=self.username)

        # Create the table from scratch
        if not update:
            heading_name = ["Num", "Movie", "Date", "Time", "Location"]     # Heading for my table

            self.table["show"] = "headings"
            self.table["columns"] = list(range(len(heading_name)))

            for i in range(len(heading_name)):
                self.table.heading(i, text=heading_name[i])

            for i in range(len(self.all_info)):
                self.table.insert("", 'end', text="L1", values=(i + 1, self.all_info[i][0], self.all_info[i][1],
                                                                self.all_info[i][2], self.all_info[i][9]))

            # I am adjusting the table structure
            self.table.column(0, anchor="center", width=60)
            self.table.column(1, anchor="center", width=250)
            self.table.column(2, anchor="center", width=150)
            self.table.column(3, anchor="center", width=120)
            self.table.column(4, anchor="center")
        else:
            # Clear the table first before adding to the table
            for i in self.table.get_children():
                self.table.delete(i)

            # Fill in the table with new data
            for i in range(len(self.all_info)):
                self.table.insert("", 'end', text="L1", values=(i + 1, self.all_info[i][0], self.all_info[i][1],
                                                                self.all_info[i][2], self.all_info[i][9]))


def get_booked_tickets(username):
    """get_booked_tickets(username) --->
    return list which has information for the table and information for the ticket info
    -username is one of the parameter for the function (The user's Username)
    -Checks all the database from cinema_location = ["London", "Canary Wharf", "The O2 Arena", "Waterloo"] and see if the
     customer_tickets table in the database has that username tickets.
    """

    # Getting the userID first
    global userDB_path, cinema_location
    db = sqlite3.connect(userDB_path)
    cursor = db.cursor()
    cursor.execute(f"""SELECT userID FROM people WHERE username = ?""", (username,))
    userID = cursor.fetchone()[0]  # UserId Obtained
    db.close()

    # I am going through all the database searching for booked movies

    all_info = []  # Store it here. We get list inside a list
    for location in cinema_location:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{location}.db"))
        db = sqlite3.connect(path)
        cursor = db.cursor()

        cursor.execute("""SELECT m.name, s.date, s.time, s.cinema_hall, c.num_tickets, c.adult_tickets, c.child_tickets, c.user_tickets, c.cost
           FROM movie m, schedule s, customer_tickets c
           WHERE c.userID = ?
           AND c.scheduleID = s.scheduleID
           AND s.movieID == m.movieID""", (userID,))

        temp = cursor.fetchall()

        # Add into the list if it is not empty

        if temp:
            all_info += [list(i) + [location] for i in temp]  # adding to the list

        db.close()  # Closing the database

    all_info = sorted(all_info, key=lambda x: (x[1], x[2]), reverse=True)     # Sort by date then time

    info_text = [None]
    for info in all_info:
        message = f"""
        Movie: {info[0]}
        Location: {info[9]}
        Date: {info[1]}
        Time: {info[2]}
        Cinema Hall: {info[3]}
        Number Of Seats: {info[4]}
        Adult Ticket {"s" if int(info[5]) > 1 else ""}: {info[5]}
        Child Ticket{"s" if int(info[6]) > 1 else ""}: {info[6]}
        Seat Location{"s" if len(info[7]) > 1 else ""}: {info[7]}
        Cost: £{info[8]} """

        info_text.append(message)

    return [all_info, info_text]