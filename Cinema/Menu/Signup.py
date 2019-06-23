from tkinter import *
from tkinter import messagebox
import sqlite3
import re
import os

userDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'User.db'))


class SignUp:
    """Signup class: A Signup window.
     - Create a user account
    "window" is a parameter: it is a window object that is passed around so we do not need to create it every single
     time"""
    def __init__(self, window):
        self.window = window
        self.window.title("Sign Up")
        self.window.geometry("900x727+300+30")

        # Background
        self.background = Label(self.window, image=self.window.img2)
        self.background.grid(row=0, column=0, rowspan=900, columnspan=727)

        self.back_btn = Button(self.window, text="Back", font=("Arial", 27), command=self.go_back, bg="#D1E3F6", bd=1)
        self.back_btn.grid(row=0, column=0, padx=(10, 120), pady=(10, 0))

        # First name
        self.first_name_display = LabelFrame(self.window, text="First Name:", font=("Arial", 15), bg="#414141", fg="white")
        self.first_name_display.grid(row=1, column=1)
        self.first_name_input = Entry(self.first_name_display, width=20, font=("Arial", 27))
        self.first_name_input.grid()
        self.first_name_input.focus()
        self.first_name_input.bind("<Return>", lambda e: self.enter())

        # Last name
        self.last_name_display = LabelFrame(self.window, text="Last Name:", font=("Arial", 15), bg="#414141", fg="white")
        self.last_name_display.grid(row=3, column=1)
        self.last_name_input = Entry(self.last_name_display, width=20, font=("Arial", 27))
        self.last_name_input.grid()
        self.last_name_input.bind("<Return>", lambda e: self.enter())

        # Username
        self.username_display = LabelFrame(self.window, text="Username:", font=("Arial", 15), bg="#414141", fg="white")
        self.username_display.grid(row=4, column=1)
        self.username_input = Entry(self.username_display, width=20, font=("Arial", 27))
        self.username_input.grid()
        self.username_input.bind("<Return>", lambda e: self.enter())

        # Password
        self.password_display = LabelFrame(self.window, text="Password:", font=("Arial", 15), bg="#414141", fg="white")
        self.password_display.grid(row=5, column=1)
        self.password_input = Entry(self.password_display, width=20, font=("Arial", 27))
        self.password_input.grid()
        self.password_input.bind("<Return>", lambda e: self.enter())

        # Re-Password
        self.re_password_display = LabelFrame(self.window, text="Re-enter Password:", font=("Arial", 15), bg="#414141", fg="white")
        self.re_password_display.grid(row=6, column=1)
        self.re_password_input = Entry(self.re_password_display, width=20, font=("Arial", 27))
        self.re_password_input.grid()
        self.re_password_input.bind("<Return>", lambda e: self.enter())

        # Age
        self.age_display = LabelFrame(self.window, text="Age:", font=("Arial", 15), bg="#414141", fg="white")
        self.age_display.grid(row=7, column=1)
        self.age_input = Entry(self.age_display, width=20, font=("Arial", 27))
        self.age_input.grid()
        self.age_input.bind("<Return>", lambda e: self.enter())

        # Email
        self.email_display = LabelFrame(self.window, text="Email:", font=("Arial", 15), bg="#414141", fg="white")
        self.email_display.grid(row=8, column=1)
        self.email_input = Entry(self.email_display, width=20, font=("Arial", 27))
        self.email_input.grid()
        self.email_input.bind("<Return>", lambda e: self.enter())

        # Mobile Number
        self.mobile_display = LabelFrame(self.window, text="Mobile number:", font=("Arial", 15), bg="#414141", fg="white")
        self.mobile_display.grid(row=9, column=1)
        self.mobile_input = Entry(self.mobile_display, width=20, font=("Arial", 27))
        self.mobile_input.grid()
        self.mobile_input.bind("<Return>", lambda e: self.enter())

        # Enter Button
        self.enter_btn = Button(self.window, text="Enter", bg="#D7BCF8", bd=2, font=("Arial", 20), command=self.enter)
        self.enter_btn.place(x=400, y=660)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.background, self.back_btn, self.first_name_display, self.first_name_input,
                        self.last_name_display, self.last_name_input, self.username_input, self.username_display,
                        self.password_input, self.password_display, self.re_password_display, self.re_password_input,
                        self.email_display, self.email_input, self.mobile_display, self.mobile_input,
                        self.age_display, self.age_input, self.enter_btn]

    def is_valid_input(self):
        """
        is_valid_input() will validate your sign up info. If all the user detail is correct return True
        else return False.

        - I use regex to validate name, username, password and email
        - Checks is username or email exist in the database. If true --> Invalid
        - age >= 16 and age <100
        - check if the password and re-type password matches
        - email should have @, . and other stuff (by using regex)
        - username has a min 2 character and max 20 character
        - Password should have min of 5 character, at least 1 upper case and 1 number
        - Email has max 255 character
        - Mobile number should be all number and the length of number it should be between 10-13
        """
        global userDB_path
        db = sqlite3.connect(userDB_path)

        cursor = db.cursor()
        cursor.execute("""SELECT username FROM people WHERE username = ? """, (self.username_input.get(),))
        username_check = cursor.fetchall()
        cursor.execute("""SELECT email FROM people WHERE email = ?""", (self.email_input.get(),))
        email_check = cursor.fetchall()

        while True:
            # Letters in the first name should be an alphabet
            if not bool(re.match("[A-Za-z]{2,20}( [A-Za-z]{2,20})?", self.first_name_input.get())):
                self.first_name_input.config(bg="#E96A6A")
                messagebox.showwarning("Invalid", "Your first name has invalid character.")
                self.first_name_input.config(bg="white")
                break
            # Checks the length of the the first name
            if len(self.first_name_input.get()) < 2 or len(self.first_name_input.get()) > 20:
                self.first_name_input.config(bg="#E96A6A")
                if len(self.first_name_input.get()) < 2:
                    messagebox.showwarning("Invalid", "Your first name is too small.")
                else:
                    messagebox.showwarning("Invalid", "Your first name is too big.")
                self.first_name_input.config(bg="white")
                break

            # Letters in the last name should be an alphabet
            if not bool(re.match("[A-Za-z]{2,20}( [A-Za-z]{2,20})?", self.last_name_input.get())):
                self.last_name_input.config(bg="#E96A6A")
                messagebox.showwarning("Invalid", "Your Last name has invalid character.")
                self.last_name_input.config(bg="white")
                break

            # Checks the length of the the last name
            if len(self.last_name_input.get()) < 2 or len(self.last_name_input.get()) > 20:
                self.last_name_input.config(bg="#E96A6A")
                if len(self.last_name_input.get()) < 2:
                    messagebox.showwarning("Invalid", "Your last name is too small.")
                else:
                    messagebox.showwarning("Invalid", "Your last name is too big.")
                self.last_name_input.config(bg="white")
                break

            # If the username is empty or too small
            if len(self.username_input.get()) == 0 or 20 < len(self.username_input.get()) < 3:
                self.username_input.config(bg="#E96A6A")
                if len(self.username_input.get()) == 0:
                    messagebox.showerror("Invalid", "Please enter  username.")
                elif len(self.username_input.get()) < 3:
                    messagebox.showerror("Invalid", "The length of the username is too small.")
                else:
                    messagebox.showerror("Invalid", "The length of the username is too big.")
                self.username_input.config(bg="white")
                break

            # For username, only number and letter are valid. No spaces and other character
            if not bool(re.match("^[a-zA-Z0-9*]+$", self.username_input.get())):
                self.username_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Invalid username.")
                self.username_input.config(bg="white")
                break

            # Check if the username already exist in the database
            if username_check:
                self.username_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Username already exists. Try again")
                self.username_input.config(bg="white")
                break

            # Password should have number and alphabet
            if not bool(re.match("[A-Za-z0-9]+", self.password_input.get())):
                self.password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Password has invalid character.\nPassword should only have letters and numbers.")
                self.password_input.config(bg="white")
                break

            # Checks the strength of the password
            if len(self.password_input.get()) < 5 or not (
                    any(letter.isupper() for letter in self.password_input.get())) or not (
                    any(num.isnumeric() for num in self.password_input.get())):
                self.password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Password not strong enough."
                                                "\nPassword must be at least 5 letter long."
                                                "\nPassword must have at lest 1 capital letter and 1 number."
                                                "\nTry again.")
                self.password_input.config(bg="white")
                break

            # Check if the passwords written are the same
            if self.password_input.get() != self.re_password_input.get():
                self.re_password_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Password not same. Try again")
                self.re_password_input.config(bg="white")
                break

            # Check if the age is a number or if the age is greater than 2 digit number
            if not (self.age_input.get().isnumeric()) or len(self.age_input.get()) > 2:
                self.age_input.config(bg="#E96A6A")
                messagebox.showwarning("Invalid", "Invalid age.")
                self.age_input.config(bg="white")
                break

            # Valid age. Check if your are eligible to create an account
            if int(self.age_input.get()) < 16 or int(self.age_input.get()) > 100:
                self.age_input.config(bg="#E96A6A")
                if int(self.age_input.get()) < 16:
                    messagebox.showwarning("Invalid", "You are under 16 years of age. You can not sign up.")
                else:
                    messagebox.showwarning("Invalid", "Invalid Age")
                self.age_input.config(bg="white")
                break

            # Start should be a letter (so no spaces, number), also you can not have spaces in between your email
            if not bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email_input.get())):
                self.email_input.config(bg="#E96A6A")
                messagebox.showinfo("Invalid", "Invalid email address.")
                self.email_input.config(bg="white")
                break

            # Check if the email given already exists in database
            if email_check:
                self.email_input.config(bg="#E96A6A")
                messagebox.showerror("Invalid", "Email already exists. Try again")
                self.email_input.config(bg="white")
                break

            # Checks if the email length is too big
            if len(self.email_input.get()) > 255:
                self.email_input.config(bg="#E96A6A")
                messagebox.showwarning("Invalid", "Your email is too big.")
                self.email_input.config(bg="white")
                break

            # Validate mobile number
            if not (self.mobile_input.get()).isnumeric() or not (10 <= len(self.mobile_input.get()) <= 13):
                self.mobile_input.config(bg="#E96A6A")
                messagebox.showwarning("Invalid", "Invalid mobile number.")
                self.mobile_input.config(bg="white")
                break

            # If all the info are valid then return true.
            return True

        return False

    def enter(self):
        """enter() if check_input() returns true --> enter_in_database() will add the new user to the database"""
        if self.is_valid_input():
            first_name = self.first_name_input.get()
            last_name = self.last_name_input.get()
            username = self.username_input.get()
            password = self.password_input.get()
            email = self.email_input.get()
            age = self.age_input.get()
            mobile = self.mobile_input.get()

            self.enter_in_database(username=username, password=password, first_name=first_name, last_name=last_name,
                                   email=email, mobile=mobile, age=age)
            messagebox.showinfo("Welcome", "Your account has been created.")

    @staticmethod
    def enter_in_database(username, password, first_name, last_name, email, mobile, age):
        """enter_in_database() will add the new user in the database"""
        global userDB_path
        db = sqlite3.connect(userDB_path)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO people(username, password, first_name, last_name, email, phone, age)
        VALUES(?, ?, ?, ?, ?, ?, ?)""", (username, password, first_name, last_name, email, mobile, age))
        db.commit()
        db.close()

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]

    def go_back(self):
        """go_back() takes you back to the menu. First destroy all the widget (clearing the window)"""
        self.destroy_all()
        self.window.geometry("900x600")
        self.window.menuHome(window=self.window)
