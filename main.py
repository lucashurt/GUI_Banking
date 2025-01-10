import sys
from login_register import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoginWindow()
    MainDialog = QDialog()
    ui.show()
    sys.exit(app.exec())
