from tkinter import *
from Menu.Login import Login as LoginWindow
from Menu.Signup import SignUp as SignUPWindow


class Menu:
    """Menu class: A Menu window.
     - Press login to goto the login window
     - Press signup to goto the Signup window
    "window": it is a Tk() object (tkinter object) that is passed around so we do not need to create it every single
     time
     If window=None create the Tk() object for the first time
     """

    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
            self.window.geometry("900x600+300+30")
            self.window.resizable(False, False)
        else:
            self.window = window

        self.window.title("Welcome")

        self.window.menuHome = Menu
        self.window.menuSign = SignUPWindow
        self.window.menuLogin = LoginWindow

        # Picture
        self.window.img1 = PhotoImage(file="image/Menu.gif")
        self.window.img2 = PhotoImage(file="image/Signup.gif")
        self.background = Label(self.window, image=self.window.img1, width=900, height=600)
        self.background.grid(row=0, column=0, rowspan=900, columnspan=600)

        # Login Button
        self.login_btn = Button(self.window, text="Login", bg="#F2D2AD", bd=3, font=("Arial", 40), command=self.login)
        self.login_btn.grid(column=1, row=4, pady=(250, 20), padx=(350, 0))

        # Signup Button
        self.signup_btn = Button(self.window, text="Signup", bd=3, bg="#B4ADFD", font=("Arial", 40), command=self.signup)
        self.signup_btn.grid(column=1, row=5, padx=(350, 0))

        # All the widget I created, I store it here. So i can easily destroy them later.
        self.widgets = [self.login_btn, self.signup_btn]

        self.window.mainloop()

    def login(self):
        """login takes you to the login page"""
        self.destroy_all()
        self.window.menuLogin(window=self.window)

    def signup(self):
        """signup takes you to the Signup page"""
        self.destroy_all()
        self.background.destroy()
        self.window.menuSign(window=self.window)

    def destroy_all(self):
        """ destroy_all() Destroys all the widget (Clears the window, so I can use the same window for adding new
         widgets) """
        [widget.destroy() for widget in self.widgets]
