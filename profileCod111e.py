import sys
from PyQt5 import QtGui, QtCore

class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.username = QtGui.QLineEdit()
        self.password = QtGui.QLineEdit()
        loginLayout = QtGui.QFormLayout()
        loginLayout.addRow("Username", self.username)
        loginLayout.addRow("Password", self.password)

        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):
        if str(self.password.text()) == "12345": # do actual login check
            self.accept()
        else:
            pass # or inform the user about bad username/password


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.label = QtGui.QLabel()
        self.setCentralWidget(self.label)

    def setUsername(self, username):
        # do whatever you want with the username
        self.username = username
        self.label.setText("Username entered: %s" % self.username)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    login = LoginDialog()
    if not login.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)

    # 'accept': continue
    main = MainWindow()
    main.setUsername(login.username.text()) # get the username, and supply it to main window
    main.show()

    sys.exit(app.exec_())