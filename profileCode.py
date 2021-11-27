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

    def closeEvent(self, event):
        self.login_edit.setText('')
        self.password_edit.setText('')
        self.error_label.setText('')
        event.accept()


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrationUI.ui', self)
        self.db = DBManager()
        self.reg_complete.clicked.connect(self.trytoreg)
        self.man_radio.toggle()

    def trytoreg(self):
        if self.db.add_user(self.login_edit.text(), self.password_edit.text(), self.firstname_edit.text(),
                            self.lastname_edit.text(), self.check_gender()) == 'Пользователь создан':
            self.close()
        else:
            self.error_label.setText('Такой логин уже занят!')

    def check_gender(self):
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'

    def closeEvent(self, event):
        self.login_edit.setText('')
        self.password_edit.setText('')
        self.firstname_edit.setText('')
        self.lastname_edit.setText('')
        self.error_label.setText('')
        self.man_radio.toggle()
        event.accept()


class Settings(QWidget):
    id = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__()
        self.ui = uic.loadUi('settingsUI.ui', self)
        self.db = DBManager()
        self.man_radio.toggle()
        self.parent = parent
        self.save_button.clicked.connect(self.apply)

    def apply(self):
        login = self.parent.login.text()
        if self.db.change_user_data(login, self.firstname_edit.text(), self.lastname_edit.text(),
                                    self.check_gender()) == 'Данные акаунта изменены':
            ok = True
        else:
            self.error_label.setText('Ошибка')
        if self.db.change_password(login, self.password_edit.text()) == 'Пароль изменен' and ok is True:
            self.id.emit(self.db.find_user_line(login)['id'])
            self.close()
        else:
            self.error_label.setText('Ошибка')

    def check_gender(self):
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'

    def call(self):
        self.show()

    def closeEvent(self, event):
        self.password_edit.setText('')
        self.firstname_edit.setText('')
        self.lastname_edit.setText('')
        self.man_radio.toggle()
        event.accept()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('profileUI.ui', self)
        self.db = DBManager()
        self.hiding(True)
        self.registr = Registration()
        self.log = Login()
        self.settings = Settings(self)
        self.log.id[int].connect(self.apply)
        self.settings.id[int].connect(self.apply)
        self.registr_but.clicked.connect(self.registr.show)
        self.log_but.clicked.connect(self.log.show)
        self.editButton.clicked.connect(self.settings.call)
        self.exitButton.clicked.connect(lambda: self.hiding(True))

    def hiding(self, hide):
        elements = [self.count, self.count1, self.facEdit, self.selected_fac, self.selected_vuz, self.vuzEdit,
                    self.photoLabel, self.firstname_label, self.lastname_label, self.exitButton, self.editButton,
                    self.login, self.login_label, self.gender, self.gender_label]
        if hide is True:
            for i in elements:
                i.hide()
            self.log_but.show()
            self.registr_but.show()
        else:
            for i in elements:
                i.show()
            self.log_but.hide()
            self.registr_but.hide()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
