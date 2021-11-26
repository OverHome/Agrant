import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QWidget
from DBManager import DBManager


class Login(QWidget):
    id = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        uic.loadUi('loginUI.ui', self)
        self.db = DBManager()
        self.enterButton.clicked.connect(self.check)
        self.error_label.hide()

    def check(self):
        result = self.db.sign_in(self.login_edit.text(), self.password_edit.text())
        if result == 'Неверный пароль':
            self.error_label.setText('Неверный пароль')
            self.error_label.show()
        elif result == "Пользователя не существует":
            self.error_label.setText("Пользователя не существует")
            self.error_label.show()
        else:
            self.id.emit(result)
            self.close()


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrationUI.ui', self)
        self.db = DBManager()
        self.reg_complete.clicked.connect(self.trytoreg)
        self.error_label.hide()

    def trytoreg(self):
        if self.db.add_user(self.login_edit.text(), self.password_edit.text(), self.firstname_edit.text(),
                            self.lastname_edit.text(), self.check_gender()) == 'Пользователь создан':
            self.close()
        else:
            self.error_label.show()

    def check_gender(self):
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('profileUI.ui', self)
        self.db = DBManager()
        self.hiding(True)
        self.registr = Registration()
        self.log = Login()
        self.log.id[int].connect(self.apply)
        self.registr_but.clicked.connect(self.registr.show)
        self.log_but.clicked.connect(self.log.show)

    def change_user_data(self):
        if self.db.add_user(self.login_edit.text(), self.firstname_edit.text(),
                            self.lastname_edit.text(), self.check_gender()) == "Пользователь создан":
            self.save_condit.setText('1')
        else:
            self.save_condit.setText('0')

    def check_gender(self):
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'

    def hiding(self, hide):
        elements = [self.count, self.count1, self.facEdit, self.selected_fac, self.selected_vuz, self.vuzEdit,
                    self.photoLabel, self.firstname_label, self.lastname_label, self.exitButton, self.editButton,
                    self.login, self.login_label, self.gender, self.gender_label]
        if hide is True:
            for i in elements:
                i.hide()
        else:
            for i in elements:
                i.show()

    def apply(self, id):
        data = self.db.find_user_data(id)
        self.firstname_label.setText(data['first_name'])
        self.lastname_label.setText(data['last_name'])
        if data['gender'] == 'man':
            self.gender.setText('Мужской')
        else:
            self.gender.setText('Женский')
        self.login.setText(data['login'])
        self.hiding(False)
        self.log_but.hide()
        self.registr_but.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
