import sys
from PyQt6.QtWidgets import QApplication,QDialog
from home_screen import *


class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow,self).__init__()
        loadUi("login.ui",  self)
        self.login_button.clicked.connect(self.login_function)
        self.register_button.clicked.connect(self.go_to_register_screen)

    def login_function(self):
        mydb, cursor = initialize_connection()
        username = self.username_input.text()
        password = self.password_input.text()
        user_data={"username":username,"password": password}
        if login(cursor,user_data):
            self.go_to_home_screen(username)
        else:
            self.error_text.setText("Error: Incorrect Username or Password")

    def go_to_register_screen(self):
        self.username_input.clear()
        self.password_input.clear()

        self.ui = RegisterWindow()
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_home_screen(self,username):
        self.username_input.clear()
        self.password_input.clear()

        self.ui = HomeScreen(username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class RegisterWindow(QDialog):
    def __init__(self):
        super(RegisterWindow,self).__init__()
        loadUi("register.ui", self)
        self.register_button.clicked.connect(self.register_user)
        self.login_button.clicked.connect(self.go_to_login_screen)

    def register_user(self):
        mydb, cursor = initialize_connection()

        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        pin = self.PIN_input.text()
        user_data = {"name": name, "username": username, "password": password, "PIN": pin}

        for char in name:
            if not char.isalpha() and not char.isspace():
                 self.error_text.setText("Error: Name must have only letters or spaces")
                 return
        if len(name)==0 or len(username)==0 or len(password)==0 or len(pin)==0:
            self.error_text.setText("Error: No field can be left empty")
            return
        elif username_not_available(cursor, user_data):
            self.error_text.setText("Error: Username already exists")
            return
        elif len(name)>70:
            self.error_text.setText("Error: Name cannot be more than 70 characters long")
            return
        elif len(username) > 50 or len(username) < 8:
            self.error_text.setText("Error: Username must be from 8-50 characters long")
            return
        elif len(password) < 12 or len(password) > 50:
            self.error_text.setText("Error: Password must be from 12-50 characters long")
            return
        elif not pin.isdigit() or int(pin)>9999 or int(pin)<1000:
            self.error_text.setText("Error: PIN must be a 4 digit number")
            return
        else:
            register(cursor,mydb,user_data)
            self.error_text.setText(" ")
            self.go_to_home_screen(username)

    def go_to_login_screen(self):
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.PIN_input.clear()

        self.ui = LoginWindow()
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_home_screen(self,username):
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.PIN_input.clear()

        self.ui = HomeScreen(username)
        self.ui.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoginWindow()
    MainDialog = QDialog()
    ui.show()
    sys.exit(app.exec())

