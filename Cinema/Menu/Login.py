import logging
import datetime
import sqlite3
import os

from tkinter import *
from tkinter import messagebox

from Customer.C_Home import Home as C_Home
from Employee.E_Home import Home as E_Home


userDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "User.db"))


class Login:
    """Login class: A Login window
     - where you can sign in
     - it is a gateway to customer or employee window
     "window" is a parameter: it is a window object that is passed around so we do not need to create it every single
     time
     """

    def __init__(self, window):
        self.window = window
        self.window.title("Login")
        self.window.geometry("900x600")

        # Back button
        self.back_btn = Button(self.window, text="Back", font=("Arial, Bold", 30), command=self.go_back, bg="#D1E3F6", bd=1)
        self.back_btn.place(x=20, y=15)

        # Username
        self.username_display = LabelFrame(self.window, text="Username:", font=("Arial", 15), fg="white", bg="#414141")
        self.username_display.grid(row=2, column=0, pady=(180, 10), padx=(280, 0))
        self.username_input = Entry(self.username_display, width=18, font=("Arial", 30), bg="white")
        self.username_input.grid()
        self.username_input.bind("<Return>", lambda e: self.enter())
        self.username_input.focus()

        # Password
        self.password_display = LabelFrame(self.window, text="Password:", font=("Arial", 15), fg="white", bg="#414141")
        self.password_display.grid(row=3, column=0, padx=(280, 0))
        self.password_input = Entry(self.password_display, width=18, font=("Arial", 30), show="*", bg="white")
        self.password_input.grid()
        self.password_input.bind("<Return>", lambda e: self.enter())

        # Enter button
        self.login_btn = Button(self.window, text="Login", bd=1, font=("Arial", 25), command=self.enter, bg="#D7BCF8")
        self.login_btn.place(x=430, y=380)

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.back_btn, self.username_display, self.username_input, self.password_display,
                        self.password_input, self.login_btn]

    def enter(self):
        """
        enter() checks if the user exist or not. Then if it exists, check if it is a customer or an employee.
        If it is a customer, then it takes you to the customer page.
        If it is an employee, checks which branch of cinema the employee works at then it takes you to the employee page
        """

        username = self.username_input.get()
        password = self.password_input.get()
        # if authenticate(username=username, password=password)

        global userDB_path
        db = sqlite3.connect(userDB_path)
        cursor = db.cursor()
        cursor.execute("""SELECT username, password, employee, branch
                          FROM people WHERE username = ? and password = ?""",
                       (username, password))
        temp = cursor.fetchone()
        if temp:
            self.window.withdraw()
            self.password_input.delete(0, "end")  # Removes the password
            self.password_input.focus()

            if temp[2]:  # Employee
                E_Home(old_window=self.window, username=username, location=temp[3])
            else:  # Customer
                logging.basicConfig(level=logging.INFO, filename="logging.log")
                logging.info(f"Username: {username} Login {datetime.datetime.now()}")
                C_Home(old_window=self.window, username=username)

        else:
            messagebox.showerror("Invalid", "Username and Password are incorrect.")

        db.close()

    def go_back(self):
        """go_back() takes you back to the menu. First destroy all the widget (clearing the window)"""
        self.destroy_all()
        self.window.menuHome(window=self.window)

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
        widgets) """
        [widget.destroy() for widget in self.widgets]

