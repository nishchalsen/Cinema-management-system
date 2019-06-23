from tkinter import *
import sqlite3
import os
import logging
import datetime
from tkinter import messagebox

userDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'User.db'))


class User:
    """User class: Booking window.
         - See your User Info (name, age, email, mobile, ....)
         - Change your password
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
    time
    old_window: reference to the tk() object (Login window)
    username: User's username -_-
    If customer=True You get a customer view
    If customer=False You get a employee view
     """
    def __init__(self, window, old_window, username, customer=False):
        self.username = username
        self.old_window = old_window

        self.customer = customer
        self.window = window
        self.window.title("Booked")

        self.all_info = get_all_info(username=username)

        if customer:
            # Customers Options
            self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5", command=self.goto_home)
            self.home.grid(row=0, column=0, padx=(15, 10))
            self.booking = Button(self.window, text=" Booking ", font=("Arial", 30), bd=0, bg="#CA65F5",
                                  command=self.goto_booking)
            self.booking.grid(row=0, column=1, padx=(0, 10))
            self.booked = Button(self.window, text=" Booked ", font=("Arial", 30), bd=0, bg="#1F8BF3",
                                 command=self.goto_booked)
            self.booked.grid(row=0, column=2, padx=(0, 10))
            self.user = Button(self.window, text=" User ", font=("Arial", 30), bd=0, bg="#BDC3C7")
            self.user.grid(row=0, column=3, padx=(0, 10))
            self.sign_out = Button(self.window, text=" Sign Out ", font=("Arial", 30), bd=0, bg="#FF916E",
                                   command=self.goto_sign_out)
            self.sign_out.grid(row=0, column=4, padx=(0, 10))

            self.heading = [self.home, self.booked, self.booking, self.user, self.sign_out]
        else:
            self.home = Button(self.window, text="Home", font=("Arial", 30), bd=0, bg="#CBFBB5", command=self.goto_home)
            self.home.grid(row=0, column=0, padx=(15, 10))
            self.add_movie = Button(self.window, text=" Movie ", font=("Arial", 30), bd=0, bg="#1F8BF3",
                                    command=self.goto_add_movie)
            self.add_movie.grid(row=0, column=1, padx=(0, 10))
            self.cinema_schedule = Button(self.window, text=" Scheduling ", font=("Arial", 30), bd=0, bg="#CA65F5",
                                          command=self.goto_cinema_schedule)
            self.cinema_schedule.grid(row=0, column=2, padx=(0, 10))
            self.user = Button(self.window, text=" User ", font=("Comic Sans", 30), bd=0, bg="#BDC3C7")
            self.user.grid(row=0, column=3, padx=(0, 10))
            self.sign_out = Button(self.window, text=" Sign Out", font=("Comic Sans", 30), bd=0, bg="#FF916E",
                                   command=self.goto_sign_out)
            self.sign_out.grid(row=0, column=4, padx=(0, 10))

            self.heading = [self.home, self.add_movie, self.cinema_schedule, self.user, self.sign_out]

        # Profile Picture
        self.picture = Label(self.window, image=self.window.profile_pic, bg="silver", bd=5)
        self.picture.place(x=500, y=100)

        # Username
        self.username_display = LabelFrame(self.window, text="Username:", font=("Arial", 10), bg="#414141", fg="white")
        self.username_display.place(x=80, y=100)
        self.username_lbl = Label(self.username_display, text=self.all_info["username"], font=("Arial", 20), width=20)
        self.username_lbl.grid()

        # First name
        self.first_name_display = LabelFrame(self.window, text="First Name:", font=("Arial", 10), bg="#414141",
                                             fg="white")
        self.first_name_display.place(x=80, y=155)
        self.first_name_lbl = Label(self.first_name_display, text=self.all_info["first_name"], font=("Arial", 20),
                                    width=20)
        self.first_name_lbl.grid()

        # Last name
        self.last_name_display = LabelFrame(self.window, text="Last Name:", font=("Arial", 10), bg="#414141",
                                            fg="white")
        self.last_name_display.place(x=80, y=210)
        self.last_name_lbl = Label(self.last_name_display, text=self.all_info["last_name"], font=("Arial", 20),
                                   width=20)
        self.last_name_lbl.grid()
        # Age
        self.age_display = LabelFrame(self.window, text="Age:", font=("Arial", 10), bg="#414141", fg="white")
        self.age_display.place(x=80, y=265)
        self.age_lbl = Label(self.age_display, text=self.all_info["age"], font=("Arial", 20), width=5)
        self.age_lbl.grid()

        # Email
        self.email_display = LabelFrame(self.window, text="Email:", font=("Arial", 10), bg="#414141", fg="white")
        self.email_display.place(x=80, y=320)
        self.email_lbl = Label(self.email_display, text=self.all_info["email"], font=("Arial", 20), width=20)
        self.email_lbl.grid()

        # Mobile Number
        self.mobile_display = LabelFrame(self.window, text="Mobile number:", font=("Arial", 10), bg="#414141",
                                         fg="white")
        self.mobile_display.place(x=80, y=375)
        self.mobile_lbl = Label(self.mobile_display, text=self.all_info["mobile"], font=("Arial", 20), width=20)
        self.mobile_lbl.grid()

        # Change Password button
        self.change_password_btn = Button(self.window, text="Change\nPassword", font=("Arial", 15), bd=1, bg="#C9A594",
                                          fg="#3F3F3F", command=self.change_password, width=10, height=3)
        self.change_password_btn.place(x=80, y=450)

        # Type your current password
        self.current_password_display = LabelFrame(self.window, text="Enter your current password:", font=("Arial", 10),
                                                   bg="#414141", fg="white")
        self.current_password_input = Entry(self.current_password_display, font=("Arial", 15), width=20)
        self.current_password_input.bind("<Return>", lambda e: self.enter())

        # Type your new password
        self.new_password_display = LabelFrame(self.window, text="Enter your new password:", font=("Arial", 10),
                                               bg="#414141", fg="white")
        self.new_password_input = Entry(self.new_password_display, font=("Arial", 15), width=20)
        self.new_password_input.bind("<Return>", lambda e: self.enter())

        # Retype your new password
        self.retype_password_display = LabelFrame(self.window, text="Retype your new password:", font=("Arial", 10),
                                                  bg="#414141", fg="white")
        self.retype_password_input = Entry(self.retype_password_display, font=("Arial", 15), width=20)
        self.retype_password_input.bind("<Return>", lambda e: self.enter())

        # Enter Button
        self.enter_btn = Button(self.window, text="Enter", font=("Arial", 15), bd=1, command=self.enter)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.picture, self.username_display, self.username_lbl, self.first_name_display,
                        self.first_name_lbl,
                        self.last_name_display, self.last_name_lbl, self.age_display, self.age_lbl, self.email_display,
                        self.email_lbl, self.mobile_display, self.mobile_lbl, self.change_password_btn,
                        self.current_password_display, self.current_password_input, self.new_password_display,
                        self.new_password_input, self.retype_password_display, self.retype_password_input,
                        self.enter_btn] + self.heading


    def change_password(self):
        """change_option() --> enable you to change the password
        Change the "Change Password" button to "cancel" button
        Show current password, new password, re-type new password and enter button
        """

        self.change_password_btn.configure(text="Cancel", command=self.cancel)
        self.current_password_display.place(x=220, y=460)
        self.current_password_input.grid()
        self.current_password_input.focus()
        self.new_password_display.place(x=500, y=460)
        self.new_password_input.grid()
        self.retype_password_display.place(x=500, y=520)
        self.retype_password_input.grid()
        self.enter_btn.place(x=750, y=460)

    def cancel(self):
        """
        cancel() --> disable change password
        Change the "Cancel" button to "Change Password" button
        Hide current password, new password, re-type new password and enter button
        """

        self.change_password_btn.configure(text="Change\nPassword", command=self.change_password)
        # Hide Labels
        self.current_password_display.place_forget()
        self.current_password_input.grid_forget()
        self.new_password_display.place_forget()
        self.new_password_input.grid_forget()
        self.retype_password_display.place_forget()
        self.retype_password_input.grid_forget()
        self.enter_btn.place_forget()

    def enter(self):
        """enter() --> check if the password is valid or not. If valid --> update the user password in the database
        and hide the change the password.
        """
        if self.is_valid_input():
            if messagebox.askyesno("Confirm", "Are you sure you want to change your old password?"):
                update_password(username=self.username, new_password=self.new_password_input.get())
                messagebox.showinfo("Complete", "Password Changed")
                self.current_password_input.delete(0, END)
                self.new_password_input.delete(0, END)
                self.retype_password_input.delete(0, END)
                # Reset the layout
                self.cancel()


    def is_valid_input(self):
        """ is_valid_input() will validate your new and old password. If all the condition for valid password hold
        it return True else return False.
        - Password should have min of 5 character, at least 1 upper case and 1 number
        - Check if the old password given is correct
        - Check if new password == re-type new password
        """
        while True:
            # Checks if the current password input is empty
            if len(self.current_password_input.get()) == 0:
                self.current_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Please enter your current password.")
                self.current_password_input.config(bg="white")
                break

            # Check if the current password matches the actual password
            if not is_password(username=self.username, password=self.current_password_input.get()):
                self.current_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Your current password is wrong.")
                self.current_password_input.config(bg="white")
                break

            # Checks if the new password input is empty
            if len(self.new_password_input.get()) == 0:
                self.new_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Please enter your new password.")
                self.new_password_input.config(bg="white")
                break

            # The new password should not be the same as the current password
            if self.new_password_input.get() == self.current_password_input.get():
                self.new_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Your new password should not be the same as your current password.")
                self.new_password_input.config(bg="white")
                break
            # Validate the password
            if not bool(re.match("[A-Za-z0-9]+", self.new_password_input.get())):
                self.new_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid",
                                     "Password has invalid character.\nPassword should only have letters and numbers.")
                self.new_password_input.config(bg="white")
                break

            # Checks the strength of the password
            if len(self.new_password_input.get()) < 5 or not (
                    any(letter.isupper() for letter in self.new_password_input.get())) or not (
                    any(num.isnumeric() for num in self.new_password_input.get())):
                self.new_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Password not strong enough."
                                                "\nPassword must be at least 5 letter long."
                                                "\nPassword must have at lest 1 capital letter and 1 number."
                                                "\nTry again.")
                self.new_password_input.config(bg="white")
                break

            # Check if the passwords written are the same
            if self.new_password_input.get() != self.retype_password_input.get():
                self.retype_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Password not same. Try again")
                self.retype_password_input.config(bg="white")
                break
            return True

    def goto_home(self):
        """Takes you to the Home window"""

        self.destroy_all()
        self.window.Home(window=self.window, old_window=self.old_window, username=self.username)

    def goto_booked(self):
        """Takes you to the Booked window"""

        self.destroy_all()
        self.window.Booked(window=self.window, old_window=self.old_window, username=self.username)

    def goto_booking(self):
        """Takes you to the booking window"""

        self.destroy_all()
        self.window.Booking(window=self.window, old_window=self.old_window, username=self.username)

    def goto_add_movie(self):
        """Takes you to the add movie window"""

        self.destroy_all()
        self.window.Movie(username=self.username, window=self.window, old_window=self.old_window)

    def goto_cinema_schedule(self):
        """Takes you to the cinema schedule window"""

        self.destroy_all()
        self.window.Scheduling(username=self.username, window=self.window, old_window=self.old_window)

    def goto_sign_out(self):
        """Signs out the user and takes the user back to the Login menu.
        If is it is a customer, it logs the date and time when you sign out"""

        if self.customer:
            logging.basicConfig(level=logging.INFO, filename="logging.log")
            logging.info(f"Username: {self.username} Sign-out {datetime.datetime.now()}")
        self.window.destroy()
        self.old_window.deiconify()

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]


def get_all_info(username):
    """get_all_info(username) --> return a dicitonary of user information key=info_type(like email, age, ...)
    value=info_value(age=15)
    username is the one parameter of the function (which is just user Username)"""

    global userDB_path
    db = sqlite3.connect(userDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT username, first_name, last_name, email, age, phone
    FROM people WHERE username=?""", (username,))
    information = cursor.fetchone()
    all_info = {"username": information[0], "first_name": information[1], "last_name": information[2],
                "email": information[3],
                "age": information[4], "mobile": information[5]}
    db.close()
    return all_info


def is_password(username, password):
    """is_password(username, password) --> returns True or False
    username and password are the parameter of the function.
    Check if the password given matches with the user's actual password by checking if the username and password
    exist in the database
    if exist --> return True, else --> return False
    """
    global userDB_path
    db = sqlite3.connect(userDB_path)
    cursor = db.cursor()
    cursor.execute("""SELECT username FROM people
                        WHERE username=? AND password=?""", (username, password))
    temp = cursor.fetchone()
    db.close()
    return bool(temp)


def update_password(username, new_password):
    """update_password(username, new_password) --> update the user's password in the database
    username and new_password is the two parameter of the function.
    username is user's username and new_password is the user's new password"""
    global userDB_path
    db = sqlite3.connect(userDB_path)
    cursor = db.cursor()
    cursor.execute("""UPDATE people SET password=? WHERE username=?""",
                   (new_password, username))
    db.commit()
    db.close()
