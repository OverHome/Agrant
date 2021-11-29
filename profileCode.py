import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *

from DBManager import DBManager


class Login(QWidget):
    id = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        uic.loadUi('loginUI.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
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
        self.setWindowModality(QtCore.Qt.ApplicationModal)
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


class Special(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.ui = uic.loadUi('specUi.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.save_button.clicked.connect(lambda: self.save())
        self.parent = parent

    def update(self):
        self.labels = [self.rus_spin, self.maths_spin, self.phys_spin, self.chem_spin, self.history_spin, self.obs_spin,
                       self.it_spin, self.biol_spin, self.geog_spin, self.eng_spin, self.liter_spin, self.achiv_spin]
        self.names = ["russian_language", "mathematics", "physics", "chemistry", "history", "social_studies",
                      "ICT", "biology", "geography", "foreign_languages", "literature", "achievements"]
        x = self.db.get_USE_points(self.parent.id)
        for i in range(12):
            self.labels[i].setValue(x[self.names[i]])

    def save(self):
        self.db.set_USE_points(self.parent.id, {'russian_language': self.rus_spin.value(),
                                                'mathematics': self.maths_spin.value(),
                                                'physics': self.phys_spin.value(),
                                                'chemistry': self.chem_spin.value(),
                                                'history': self.history_spin.value(),
                                                'social_studies': self.obs_spin.value(),
                                                'ICT': self.it_spin.value(),
                                                'biology': self.biol_spin.value(),
                                                'geography': self.geog_spin.value(),
                                                'foreign_languages': self.eng_spin.value(),
                                                'literature': self.liter_spin.value(),
                                                'achievements': self.achiv_spin.value()})
        self.close()

    def closeEvent(self, event):
        x = self.db.get_USE_points(self.parent.id)
        for i in range(12):
            self.labels[i].setValue(x[self.names[i]])
        event.accept()


class Settings(QWidget):
    id = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__()
        self.ui = uic.loadUi('settingsUI.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
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
        self.firstname_edit.setText(self.parent.name_label.text().split()[0])
        self.lastname_edit.setText(self.parent.name_label.text().split()[1])
        if self.parent.gender.text() == 'Женский':
            self.woman_radio.toggle()
        self.show()

    def closeEvent(self, event):
        self.password_edit.setText('')
        self.firstname_edit.setText('')
        self.lastname_edit.setText('')
        self.man_radio.toggle()
        event.accept()


class SpecPriority(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('specpriorityUI.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.parent = parent
        self.priority_list = []
        self.save_button.clicked.connect(self.save)
        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)

        widget1 = QWidget()
        self.layout1 = QVBoxLayout(widget1)
        self.layout1.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area2.setWidget(widget1)
        self.scroll_area2.setWidgetResizable(True)

        self.priority_list = []

    def load(self):
        self.priority_list.clear()
        for i in reversed(range(self.layout1.count())):
            self.layout1.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        x = self.db.get_specialties_priorities(self.parent.id)
        for i in x:
            self.priority_list.append(i['specialties'])
            label1 = QLabel()
            label1.setText(i['specialties'] + ' - ' + self.db.get_name_specialties(i['specialties']))
            self.layout1.addWidget(label1)
        y = self.db.get_specialties()
        for i in y:
            label = QCheckBox()
            label.setText(str(i[0]) + ' - ' + i[1])
            if i[0] in self.priority_list:
                label.toggle()
            label.stateChanged.connect(self.addremove)
            self.layout.addWidget(label)

    def save(self):
        self.db.set_specialties_priorities(self.parent.id, self.priority_list)
        self.close()

    def addremove(self):
        if self.sender().isChecked():
            self.priority_list.append(self.sender().text()[:8])
            self.layout1.addWidget(QLabel(self.sender().text()))
        else:
            self.priority_list.remove(self.sender().text()[:8])
            for i in reversed(range(self.layout1.count())):
                self.layout1.itemAt(i).widget().setParent(None)
            for i in self.priority_list:
                label = QLabel()
                label.setText(i + ' - ' + self.db.get_name_specialties(i))
                self.layout1.addWidget(label)

    def closeEvent(self, event):
        self.load()
        event.accept()


class UnivPriority(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('univpriorityUI.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.parent = parent
        self.priority_list = []
        self.save_button.clicked.connect(self.save)
        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)

        widget1 = QWidget()
        self.layout1 = QVBoxLayout(widget1)
        self.layout1.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area2.setWidget(widget1)
        self.scroll_area2.setWidgetResizable(True)

        self.priority_list = []

    def load(self):
        self.priority_list.clear()
        for i in reversed(range(self.layout1.count())):
            self.layout1.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        x = self.db.get_universities_priorities(self.parent.id)
        for i in x:
            self.priority_list.append(i['university'])
            label1 = QLabel()
            label1.setText(str(i['university']) + '. ' + self.db.get_university_name(i['university']))
            self.layout1.addWidget(label1)
        y = self.db.get_universities()
        for i in y:
            label = QCheckBox()
            label.setText(str(i['id']) + '. ' + i['name'])
            if i['id'] in self.priority_list:
                label.toggle()
            label.stateChanged.connect(self.addremove)
            self.layout.addWidget(label)
            z = self.priority_list

    def save(self):
        result = [int(item) for item in self.priority_list]
        self.db.set_universities_priorities(self.parent.id, result)
        self.close()

    def addremove(self):
        if self.sender().isChecked():
            self.priority_list.append(int(self.sender().text().split('.')[0]))
            self.layout1.addWidget(QLabel(self.sender().text()))
        else:
            self.priority_list.remove(int(self.sender().text().split('.')[0]))
            for i in reversed(range(self.layout1.count())):
                self.layout1.itemAt(i).widget().setParent(None)
            for i in self.priority_list:
                label = QLabel()
                label.setText(str(i) + '. ' + self.db.get_university_name(i))
                self.layout1.addWidget(label)

    def closeEvent(self, event):
        self.load()
        event.accept()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('profileUI.ui', self)
        self.setFixedSize(921, 651)
        self.db = DBManager()
        self.hiding(True)
        self.registr = Registration()
        self.log = Login()
        self.spec = Special(self)
        self.id = 3000
        self.specprior = SpecPriority(self)
        self.univprior = UnivPriority(self)
        self.settings = Settings(self)
        self.log.id[int].connect(self.apply)
        self.settings.id[int].connect(self.apply)
        self.registr_but.clicked.connect(self.registr.show)
        self.log_but.clicked.connect(self.log.show)
        self.editButton.clicked.connect(self.settings.call)
        self.exitButton.clicked.connect(lambda: self.hiding(True))
        self.facButton.clicked.connect(lambda: self.specpr())
        self.vuzButton.clicked.connect(lambda: self.univpr())

        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)

        widget1 = QWidget()
        self.layout1 = QGridLayout(widget1)
        self.layout1.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea_2.setWidget(widget1)
        self.scrollArea_2.setWidgetResizable(True)

        self.pointsButton.clicked.connect(self.special)

        self.univ = self.db.get_universities()
        for i in range(11):
            button = QPushButton()
            label2 = QLabel()
            label3 = QLabel()
            button.setText(str(i + 1) + '. ' + self.univ[i]['name'])
            button.clicked.connect(lambda: self.set_univ(i))
            label2.setText(self.univ[i]['city'])
            label3.setText(str(self.univ[i]['average_USE']))
            layout.addWidget(button, i, 1)
            layout.addWidget(label2, i, 2)
            layout.addWidget(label3, i, 3)

    def specpr(self):
        self.specprior.load()
        self.specprior.show()

    def univpr(self):
        self.univprior.load()
        self.univprior.show()

    def set_univ(self, i):
        self.heading_univ.setText(self.sender().text()[3:])
        univ_id = self.sender().text()[:1]
        self.tabWidget.setCurrentIndex(1)
        spec = self.db.get_specialties_in_university(univ_id)
        for i in reversed(range(self.layout1.count())):
            self.layout1.itemAt(i).widget().setParent(None)
        x = 1
        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l1.setText('Факультеты')
        l2.setText('Бюджетные места')
        l3.setText('Минимальный балл')
        l1.setStyleSheet("border: 3px solid black;")
        l2.setStyleSheet("border: 3px solid black;")
        l3.setStyleSheet("border: 3px solid black;")
        l1.setFont(QFont('MS Shell Dlg 2', 14))
        l2.setFont(QFont('MS Shell Dlg 2', 14))
        l3.setFont(QFont('MS Shell Dlg 2', 14))
        l1.setAlignment(QtCore.Qt.AlignCenter)
        self.layout1.addWidget(l1, 0, 0)
        self.layout1.addWidget(l2, 0, 1)
        self.layout1.addWidget(l3, 0, 2)
        for i in spec:
            label = QPushButton()
            label1 = QLabel()
            label2 = QLabel()

            label.setText(self.db.get_name_specialties(i['specialties_code']))
            label1.setText(str(i['budget_place']))
            label2.setText(str(i['pass_mark']))
            self.layout1.addWidget(label, x, 0)
            self.layout1.addWidget(label1, x, 1)
            self.layout1.addWidget(label2, x, 2)
            x += 1

    def special(self):
        self.spec.update()
        self.spec.show()

    def hiding(self, hide):
        elements = [self.photoLabel, self.name_label, self.exitButton, self.editButton,
                    self.login, self.login_label, self.gender, self.gender_label, self.pointsButton, self.facButton,
                    self.vuzButton]
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
        self.id = id
        data = self.db.find_user_data(id)
        self.name_label.setText(data['first_name'] + ' ' + data['last_name'])
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
