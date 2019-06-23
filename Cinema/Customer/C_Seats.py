from tkinter import *
from functools import partial
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
from decimal import Decimal
import os

userDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "User.db"))
cinemaDB_path = None  # Location of the cinema centre database in my directory


class ChooseSeats:
    """ChooseSeats class: ChooseSeats window.
         - Choose how many tickets you want
         - Choose which seats you want
         - See how much it cost for tickets

    old_window: reference to the tk() object (Login window)
    username: User's username -_-
    location: Location where the employee works. Use to get the database of that location
    scheduleId: Use to access and modify seating and update database
     """
    def __init__(self, username, scheduleID, old_window, location):
        global cinemaDB_path
        cinemaDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{location}.db"))

        self.old_window = old_window

        self.username = username
        self.scheduleID = scheduleID
        self.location = location
        self.cinema_info = get_cinema_info(scheduleID=scheduleID)
        self.movie_name = self.cinema_info["movie_name"]
        self.movie_time = self.cinema_info["movie_time"]
        self.movie_date = self.cinema_info["movie_date"]
        self.cinema_hall = self.cinema_info["cinema_hall"]
        self._seat_layout = seating_layout_list(self.cinema_info["cinema_layout"])
        self.available_seats = self.cinema_info["available_seats"]
        self.num_seats_chosen = 0
        self._btn_list = []
        self._temp_choice = []

        # Ticket Price
        self.adult_price = Decimal(9.20)
        self.child_price = Decimal(7.80)

        self.window = Toplevel()
        self.window.title("Choose your seats.")
        self.window.geometry("900x600+300+10")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.go_back)  # Closing the window is same as signing out


        # Background
        Label(self.window).grid(row=0, column=0, padx=(60, 0))  # Just for aligning the GUI
        self.window.bg = PhotoImage(file="image/Seating.gif")
        self.background = Label(self.window, image=self.window.bg, width=900, height=600)
        self.background.place(x=0, y=0)
        self.heading = Label(self.window, text="Choose your seats", font=("Arial", 30), bg="#D7BDE2")
        self.heading.grid(row=0, column=0, columnspan=1200, padx=(80, 0), pady=(10, 0))
        self.go_back_btn = Button(self.window, text="Go Back", command=self.go_back, font=15, bd=1, bg="#D0D3D4")
        self.go_back_btn.place(x=30, y=15)

        # Cinema Screen
        self.screen = Label(self.window, text="Screen", width=50, height=2, bg="#EBC9C2", font=20)
        self.screen.grid(row=3, column=0, columnspan=1200, pady=15, padx=(80, 0))

        # If there are available seats, enable them to book seats.
        if self.available_seats != 0:

            # Choose the number of tickets
            self.num_tickets_display = Label(self.window, text="How many movie tickets do you want:",
                                             bg="#D7BDE2", font=("Arial", 15))
            self.num_tickets_display.grid(row=1, column=0, pady=(20, 4), columnspan=50, padx=(70, 0))
            self.ticket_frame = LabelFrame(self.window, text="    Type\t       Price\t       Quantity       Sub Total         Total",
                                           fg="white", bg="#414141", font=("Arial", 12))
            self.ticket_frame.grid(row=2, column=0, columnspan=50, padx=(60, 0))
            # Adult tickets
            self.adult_ticket_lbl = Label(self.ticket_frame, text="Adult", font=("Arial", 10), fg="white", bg="#A6A6A6", width=9)
            self.adult_ticket_lbl.grid(row=0, column=0)
            self.adult_price_lbl = Label(self.ticket_frame, text=f"£{self.adult_price.quantize(Decimal('0.00'))}",
                                         fg="#EEEEEE", bg="#A6A6A6", font=("Arial", 10), width=10)
            self.adult_price_lbl.grid(row=0, column=1)
            self.adult_option = Combobox(self.ticket_frame, state="readonly", width=10)
            self.adult_option.grid(row=0, column=2)
            self.adult_option["values"] = list(range(0, self.available_seats + 1))
            self.adult_option.current(0)
            self.adult_total = Label(self.ticket_frame, text="£0.00", fg="#EEEEEE", bg="#A6A6A6", font=("Arial", 10), width=10)
            self.adult_total.grid(row=0, column=3)
            self.adult_option.bind("<<ComboboxSelected>>", lambda e: self.adult_ticket_update())
            # Children tickets
            self.child_ticket_lbl = Label(self.ticket_frame, text="Child", fg="white", bg="#A6A6A6", font=("Arial", 10), width=9)
            self.child_ticket_lbl.grid(row=1, column=0)
            self.child_price_lbl = Label(self.ticket_frame, text=f"£{self.child_price.quantize(Decimal('0.00'))}",
                                         fg="#EEEEEE", bg="#A6A6A6", font=("Arial", 10), width=10)
            self.child_price_lbl.grid(row=1, column=1)
            self.child_option = Combobox(self.ticket_frame, state="readonly", width=10)
            self.child_option.grid(row=1, column=2)
            self.child_option["values"] = list(range(0, self.available_seats + 1))
            self.child_option.current(0)
            self.child_total = Label(self.ticket_frame, text="£0.00", fg="#EEEEEE", bg="#A6A6A6", font=("Arial", 10), width=10)
            self.child_total.grid(row=1, column=3)
            self.child_option.bind("<<ComboboxSelected>>", lambda e: self.child_ticket_update())
            # Total Cost
            self.total_cost = Label(self.ticket_frame, text="£0.00", fg="#EEEEEE", bg="#A6A6A6", font=("Arial", 13), width=9, height=2)
            self.total_cost.grid(row=0, rowspan=2, column=4)

            self.enter_btn = Button(self.window, text="Enter", command=self.enter, bd=2, bg="#FAE5D3", font=("Arial", 10))
            self.enter_btn.grid(row=2, column=16)
            self.change_btn = Button(self.window, text="Change", command=self.choose_again, bd=1, bg="#FAE5D3")

            self.pay_btn = Button(self.window, text="Pay", font=15, bg="#D6EAF8", command=self.pay_function, bd=1)
            self.pay_btn.grid(row=20, column=10, pady=10, columnspan=2)
        else:
            self.no_booking = Label(self.window, text="There are no seats available.", font=("Arial", 20), bg="#F54949")
            self.no_booking.grid(row=1, column=0, pady=(20, 4), columnspan=50, padx=(70, 0))

        x, y = 1, 1
        for i in self._seat_layout:
            level = []
            for j in i:
                if j == 0:
                    btn = Button(self.window, width=5, height=2, bd=1, bg="white",
                                 command=partial(self.press_seat, (x - 1, y - 1)))
                    if x == 1:
                        btn.grid(column=x + 1, row=y + 3)
                    else:
                        btn.grid(column=x + 1, row=y + 3)
                    level.append(btn)
                elif j == 1:
                    btn = Button(self.window, width=5, height=2, bd=1, bg="grey", state="disabled",
                                 command=partial(self.press_seat, (x - 1, y - 1)))
                    btn.grid(column=x + 1, row=y + 3)
                    level.append(btn)
                else:
                    level.append(NONE)
                x += 1
            self._btn_list.append(level)

            x = 1
            y += 1

    def go_back(self):
        self.window.destroy()
        self.old_window.deiconify()

    def enter(self):
        if self.child_option.get() != "0" and self.adult_option.get() == "0":
            messagebox.showinfo("Invalid", "There must be at least one adult.")
        elif self.adult_option.get() != "0" or self.child_option.get() != "0":
            self.num_seats_chosen = int(self.adult_option.get()) + int(self.child_option.get())
            self.adult_option.configure(state="disabled")
            self.child_option.configure(state="disabled")
            self.enter_btn.configure(state="disabled")
            self.change_btn.grid(row=2, column=17, columnspan=2)
        else:
            messagebox.showinfo("Invalid", "Choose how many tickets you want, then you can choose your seats.")

    def adult_ticket_update(self):
        sub_total = Decimal(self.adult_price * int(self.adult_option.get())).quantize(Decimal('0.00'))
        self.adult_total.configure(text=f"£{sub_total}")
        self.child_option["values"] = list(range(0, (self.available_seats + 1) - int(self.adult_option.get())))
        total = Decimal(sub_total) + Decimal(self.child_price * int(self.child_option.get())).quantize(Decimal('0.00'))
        self.total_cost.configure(text=total.quantize(Decimal('0.00')))

    def child_ticket_update(self):
        sub_total = Decimal(self.child_price * int(self.child_option.get())).quantize(Decimal('0.00'))
        self.child_total.configure(text=f"£{sub_total}")
        self.adult_option["values"] = list(range(0, (self.available_seats + 1) - int(self.child_option.get())))
        total = Decimal(sub_total) + Decimal(self.adult_price * int(self.adult_option.get())).quantize(Decimal('0.00'))
        self.total_cost.configure(text=total.quantize(Decimal('0.00')))

    def pay_function(self):
        if len(self._temp_choice) == self.num_seats_chosen and self.enter_btn["state"] == "disabled":
            num_to_alph = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
            seat = ",".join([str(i[0] + 1) + str(num_to_alph[i[1]]) for i in self._temp_choice])
            message = f"""
Movie: {self.movie_name}
Location: {self.location}
Date: {self.movie_date}
Time: {self.movie_time}
Cinema Hall: {self.cinema_hall}
Number Of Seats: {len(self._temp_choice)}
Adult Ticket{"s" if int(self.adult_option.get()) > 1 else ""}: {self.adult_option.get()}
Child Ticket{"s" if int(self.child_option.get()) > 1 else ""}: {self.child_option.get()}
Seat Location{"s" if len(self._temp_choice) > 1 else ""}: {seat}
Total Cost: £{self.total_cost.cget("text")}

Are you ready to pay?"""
            if messagebox.askyesno("Confirm", message):
                global userDB_path
                db = sqlite3.connect(userDB_path)
                cursor = db.cursor()
                cursor.execute(f"""SELECT userID FROM people WHERE username = ?""", (self.username,))
                userID = cursor.fetchone()[0]
                db.close()
                new_available_seats = self.available_seats - len(self._temp_choice)
                updated_layout = seating_layout_string(self._seat_layout)

                global cinemaDB_path
                db = sqlite3.connect(cinemaDB_path)
                cursor = db.cursor()

                cursor.execute(
                    """INSERT INTO customer_tickets(userID, scheduleID, user_tickets, num_tickets, adult_tickets, child_tickets, cost)
                       VALUES(?,?,?,?,?,?,?)""",
                    (userID, self.scheduleID, seat, len(self._temp_choice), self.adult_option.get(), self.child_option.get(), self.total_cost.cget("text")))
                cursor.execute("""UPDATE seating_plan SET available_seats=?, cinema_layout=? WHERE scheduleID=?""",
                               (new_available_seats, updated_layout, self.scheduleID))

                db.commit()
                db.close()
                self.go_back()
                messagebox.showinfo("Enjoy", "Enjoy Your movie.")
        else:
            messagebox.showinfo("Invalid", "Please choose your seat first.")

    def choose_again(self):
        self.adult_option.configure(state="readonly")
        self.child_option.configure(state="readonly")
        self.enter_btn.configure(state="normal")
        self.change_btn.grid_forget()
        for pos in self._temp_choice:
            self._seat_layout[pos[1]][pos[0]] = 0
            self._btn_list[pos[1]][pos[0]].configure(bg="white")
        self._temp_choice = []
        self.num_seats_chosen = 0

    def press_seat(self, pos):
        if self._seat_layout[pos[1]][pos[0]] != 3:
            if self.num_seats_chosen != 0:
                if len(self._temp_choice) < self.num_seats_chosen:
                    self._btn_list[pos[1]][pos[0]].configure(bg="green")
                    self._seat_layout[pos[1]][pos[0]] = 3
                    self._temp_choice.append((pos[0], pos[1]))
                else:
                    messagebox.showwarning("Invalid", "You have already chosen your seats."
                                                      "\nIf you want to change it, you can do it by tapping the green square.")
            else:
                messagebox.showinfo("Invalid", "Choose how many tickets you want, then you can choose your seats.")
        else:
            self._btn_list[pos[1]][pos[0]].configure(bg="white")
            self._seat_layout[pos[1]][pos[0]] = 0
            self._temp_choice.remove((pos[0], pos[1]))


# Turn string into a list for booking
def seating_layout_list(string_layout):
    structure = []
    level = []
    for i in string_layout:
        if i == "\n":
            structure.append(level)
            level = []
        elif i == "0":
            level.append(0)
        elif i == "1":
            level.append(1)
        else:
            level.append(2)
    structure.append(level)

    return structure


# Turn list to string to store in the database
def seating_layout_string(list_layout):
    string_layout = ""
    size = len(list_layout)
    for i in range(size):
        for j in list_layout[i]:
            if j == 0:
                string_layout += "0"  # If 0, empty seat
            elif j == 1 or j == 3:
                string_layout += "1"  # If 1, seat already taken
            else:
                string_layout += "2"  # If 2, seat does not exists
        if i != size - 1:
            string_layout += "\n"
    return string_layout


def remove_seats(user_tickets, list_layout):
    alph_to_num = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    position = [(int(num[:-1]), int(alph_to_num[num[-1]])) for num in user_tickets.split(",")]
    cinema_list = seating_layout_list(list_layout)

    for x, y in position:
        cinema_list[y][x - 1] = 0

    string_layout = seating_layout_string(list_layout=cinema_list)
    return string_layout


def get_cinema_info(scheduleID):
    global cinemaDB_path
    db = sqlite3.connect(cinemaDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT m.name, s.date, s.time, sp.cinema_layout, sp.available_seats, s.cinema_hall
                      FROM seating_plan sp, schedule s, movie m
                      WHERE s.scheduleID = sp.scheduleID AND s.movieID = m.movieID
                      AND s.scheduleID=?""", (scheduleID,))
    temp = cursor.fetchone()
    db.close()
    return {"movie_name": temp[0], "movie_date": temp[1], "movie_time": temp[2], "cinema_layout": temp[3], "available_seats": temp[4], "cinema_hall": temp[5]}
