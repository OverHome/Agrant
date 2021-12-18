import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *
from PIL import Image

from Agregator import Agregator
from DBManager import DBManager


class Login(QWidget):  # Класс входа в аккаунт
    id = QtCore.pyqtSignal(int)  # Сигнал другому классу, отправляет id

    def __init__(self):  # Инициализация интерфейса
        super().__init__()
        uic.loadUi('loginUI.ui', self)
        self.setWindowTitle('Вход')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.enterButton.clicked.connect(self.check)
        self.error_label.hide()

    def check(self):  # Проверка на существование/правильный ввод логина/пароля
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

    def closeEvent(self, event):  # Закрытие окна через крестик
        self.login_edit.setText('')
        self.password_edit.setText('')
        self.error_label.setText('')
        event.accept()


class Registration(QWidget):  # Класс регистрации
    def __init__(self):  # Инициализация интерфейса
        super().__init__()
        uic.loadUi('registrationUI.ui', self)
        self.setWindowTitle('Регистрация')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.reg_complete.clicked.connect(self.trytoreg)
        self.man_radio.toggle()

    def trytoreg(self):  # Проводится проверка на пустые поля, длину вводимых данных и наличие только букв
        if not self.login_edit.text() or not self.password_edit.text() or not self.firstname_edit.text() \
                or not self.lastname_edit.text():
            self.error_label.setText('Заполнены не все поля!')
        elif self.len_check(self.login_edit.text(), 'login') is False:
            self.error_label.setText('Неправильная длина логина!')
        elif self.letter_check(self.login_edit.text(), True) is False:
            self.error_label.setText('Недопустимые символы в логине!')
        elif self.len_check(self.password_edit.text(), 'password') is False:
            self.error_label.setText('Неправильная длина пароля!')
        elif self.len_check(self.firstname_edit.text()) is False:
            self.error_label.setText('Неправильная длина имени!')
        elif self.letter_check(self.firstname_edit.text()) is False:
            self.error_label.setText('Недопустимые символы в имени!')
        elif self.len_check(self.lastname_edit.text()) is False:
            self.error_label.setText('Неправильная длина фамилии!')
        elif self.letter_check(self.lastname_edit.text()) is False:
            self.error_label.setText('Недопустимые символы в фамилии!')
        elif self.db.add_user(self.login_edit.text(), self.password_edit.text(), self.firstname_edit.text(),
                              self.lastname_edit.text(), self.check_gender()) == 'Пользователь создан':
            self.close()
        else:
            self.error_label.setText('Такой логин уже занят!')

    def len_check(self, text, type=None):  # Проверка на длину
        if len(text) > 30:
            return False
        if type == 'login' and len(text) < 5 or len(text) > 16:
            return False
        elif type == 'password' and len(text) < 8:
            return False
        elif len(text) < 2:
            return False
        return True

    def letter_check(self, text, login=False):  # Проверка на буквы
        letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwx' \
                  'yzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        if login:
            for i in text:
                if i not in letters and i not in digits:
                    return False
        elif login is False:
            for i in text:
                if i not in letters:
                    return False
        return True

    def check_gender(self):  # Метод возвращает выбранный пол
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'

    def closeEvent(self, event):  # Метод (как и многие в будущем) при закрытии профиля
        self.login_edit.setText('')
        self.password_edit.setText('')
        self.firstname_edit.setText('')
        self.lastname_edit.setText('')
        self.error_label.setText('')
        self.man_radio.toggle()
        event.accept()


class Special(QScrollArea):  # Класс настройки баллов пользователя
    def __init__(self, parent):  # Инициализация интерфейса
        super().__init__()
        self.ui = uic.loadUi('specUi.ui', self)
        self.setWindowTitle('Редактирование баллов')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.agr = Agregator()
        self.save_button.clicked.connect(lambda: self.save())
        self.parent = parent

    def update(self):  # Обновление информации в окне
        self.labels = [self.rus_spin, self.maths_spin, self.phys_spin, self.chem_spin, self.history_spin, self.obs_spin,
                       self.it_spin, self.biol_spin, self.geog_spin, self.eng_spin, self.liter_spin, self.achiv_spin]
        self.names = ["russian_language", "mathematics", "physics", "chemistry", "history", "social_studies",
                      "ICT", "biology", "geography", "foreign_languages", "literature", "achievements"]
        x = self.db.get_USE_points(self.parent.id)
        for i in range(12):
            self.labels[i].setValue(x[self.names[i]])

    def save(self):  # Сохранение введеных баллов в базу данных
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
        self.agr.start_distribution()
        self.close()

    def closeEvent(self, event):  # Закрытие окна через крестик
        x = self.db.get_USE_points(self.parent.id)
        for i in range(12):
            self.labels[i].setValue(x[self.names[i]])
        event.accept()


class Settings(QWidget):  # Класс редактирования профиля
    id = QtCore.pyqtSignal(int)  # Сигнал, содержащий id

    def __init__(self, parent):  # Инициализация класса
        super().__init__()
        self.ui = uic.loadUi('settingsUI.ui', self)
        self.setWindowTitle('Редактирование данных')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.man_radio.toggle()
        self.parent = parent
        self.pixmap = QPixmap()
        self.save_button.clicked.connect(self.apply)


    def apply(self):  # Применение введеных настроек
        login = self.parent.login.text()
        if self.db.change_user_data(login, self.firstname_edit.text(), self.lastname_edit.text(),
                                    self.check_gender()) == 'Данные акаунта изменены':
            ok = True
        else:
            self.error_label.setText('Ошибка')
            ok = False
        if 8 > len(self.password_edit.text()) or len(self.password_edit.text()) > 30:
            self.error_label.setText('Неверная длина пароля!')
        elif self.db.change_password(login, self.password_edit.text()) == 'Пароль изменен' and ok is True:
            self.id.emit(self.db.find_user_line(login)['id'])
            self.close()
        else:
            self.error_label.setText('Ошибка')

    def check_gender(self):  # Проверка на пол
        if self.man_radio.isChecked():
            return 'man'
        else:
            return 'woman'

    def call(self):  # Метод для установки данных по умолчанию в полях ввода
        self.firstname_edit.setText(self.parent.name_label.text().split()[0])
        self.lastname_edit.setText(self.parent.name_label.text().split()[1])
        if self.parent.gender.text() == 'Женский':
            self.woman_radio.toggle()
        self.show()

    def closeEvent(self, event):  # Закрытие окна крестиком
        self.password_edit.setText('')
        self.firstname_edit.setText('')
        self.lastname_edit.setText('')
        self.man_radio.toggle()
        event.accept()


class SpecPriority(QWidget):  # Класс для приоритета факультетов
    def __init__(self, parent):  # Инициализация класса
        super().__init__()
        uic.loadUi('specpriorityUI.ui', self)
        self.setWindowTitle('Приоритет факультетов')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.agr = Agregator()
        self.parent = parent
        self.priority_list = []
        self.save_button.clicked.connect(self.save)
        widget = QWidget()  # Установка полей для создания прокручиваемого поля, будет встречаться неоднократно
        self.layout = QVBoxLayout(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)

        widget1 = QWidget()
        self.layout1 = QVBoxLayout(widget1)
        self.layout1.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area2.setWidget(widget1)
        self.scroll_area2.setWidgetResizable(True)

        self.priority_list = []  # Лист приоритетов пользователя

    def load(self):  # Загрузка приоритетов
        self.priority_list.clear()
        for i in reversed(
                range(self.layout1.count())):  # При загрузке все данные приходится удалять и загружать еще раз
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
            if i[0] in self.priority_list:  # Если факультет был выбран ранее - галочка стоит по умолчанию
                label.toggle()
            label.stateChanged.connect(self.addremove)
            self.layout.addWidget(label)

    def save(self):  # Сохранение приоритетов
        self.db.set_specialties_priorities(self.parent.id, self.priority_list)
        self.agr.start_distribution()
        self.close()

    def addremove(self):  # Добавление и удаление приоритетов
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

    def closeEvent(self, event):  # Закрытие окна через крестик
        self.load()
        event.accept()


class UnivPriority(QWidget):  # Класс для приоритета ВУЗов. класс почти аналогичен предыдущему с минорными изменениями
    def __init__(self, parent):  # Инициализация интерфейса
        super().__init__()
        uic.loadUi('univpriorityUI.ui', self)
        self.setWindowTitle('Приоритет ВУЗов')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.db = DBManager()
        self.agr = Agregator()
        self.parent = parent
        self.priority_list = []
        self.save_button.clicked.connect(self.save)
        widget = QWidget()
        self.layout = QVBoxLayout(widget)  # Очередная установка поля для прокрутки
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)

        widget1 = QWidget()
        self.layout1 = QVBoxLayout(widget1)
        self.layout1.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_area2.setWidget(widget1)
        self.scroll_area2.setWidgetResizable(True)

        self.priority_list = []

    def load(self):  # Загрузка и обновление полей приоритетов
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

    def save(self):  # Сохранение приоритетов
        result = [int(item) for item in self.priority_list]
        self.db.set_universities_priorities(self.parent.id, result)
        self.agr.start_distribution()
        self.close()

    def addremove(self):  # Добавление и удаление приоритетов
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

    def closeEvent(self, event):  # Закрытие окна через крестик
        self.load()
        event.accept()


class Names(QScrollArea):  # Класс для открытия окна с именами студентов на факультете
    def __init__(self):  # Инициализация интерфейса
        super().__init__()
        uic.loadUi('namesUI.ui', self)
        self.setWindowTitle('Список учеников факультета')
        self.db = DBManager()
        widget = QWidget()
        self.layout = QGridLayout(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)

    def update(self, id, code):  # Обновление приоритетов
        self.heading.setText(self.db.get_name_specialties(code))
        names = self.db.get_enlisted_user(id, code)
        x, y = self.db.get_lessons(id, code)
        x[0] = x[0].capitalize()
        if len(y) != 0:
            self.lesson_label.setText(', '.join(x) + ', ' + ' или '.join(y))
        else:
            self.lesson_label.setText(', '.join(x))
        l1 = QLabel()
        l2 = QLabel()
        l1.setText('Имя Фамилия')
        l2.setText('Баллы')
        l1.setStyleSheet("border: 3px solid black;")
        l2.setStyleSheet("border: 3px solid black;")
        l1.setFont(QFont('MS Shell Dlg 2', 14))
        l2.setFont(QFont('MS Shell Dlg 2', 14))
        self.layout.addWidget(l1, 0, 0)
        self.layout.addWidget(l2, 0, 1)
        x = 1
        for i in range(len(names)):
            label = QLabel()
            label1 = QLabel()
            label.setFont(QFont('MS Shell Dlg 2', 14))
            label1.setFont(QFont('MS Shell Dlg 2', 14))
            label.setText(names[i]['fname'] + ' ' + names[i]['lname'])
            label1.setText(str(names[i]['points']))
            self.layout.addWidget(label, x, 0)
            self.layout.addWidget(label1, x, 1)
            x += 1

    def closeEvent(self, event):  # Закрытие окна через крестик
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        l1 = QLabel()
        l2 = QLabel()
        l1.setText('Имя Фамилия')
        l2.setText('Баллы')
        l1.setStyleSheet("border: 3px solid black;")
        l2.setStyleSheet("border: 3px solid black;")
        l1.setFont(QFont('MS Shell Dlg 2', 14))
        l2.setFont(QFont('MS Shell Dlg 2', 14))
        self.layout.addWidget(l1, 0, 0)
        self.layout.addWidget(l2, 0, 1)
        event.accept


class Profile(QMainWindow):  # Главное окно, класс профиля, списка ВУЗов и прочего
    def __init__(self):  # Инициализация интерфейса
        super().__init__()
        uic.loadUi('profileUI.ui', self)
        self.setWindowTitle('Главное окно')
        self.setFixedSize(1112, 610)
        self.db = DBManager()
        self.hiding(True)
        self.registr = Registration()
        self.log = Login()
        self.spec = Special(self)
        self.names = Names()
        self.id = None
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
        self.photo_button.clicked.connect(lambda: self.photo())

        widget = QWidget()  # Поля для прокручиваемых зон
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
        self.update_button.clicked.connect(lambda: self.priorUpdate(self.id))

        self.univ = self.db.get_universities()
        for i in range(11):  # Фиксированная установка ВУЗов (только по заранее заданному количеству)
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

    def priorUpdate(self, id):
        x = self.db.get_distributed_user(id)
        self.priorVuz_label.setText(x[0])
        self.priorSpec_label.setText(x[1])

    def specpr(self):  # Загрузка окна приоритетов факультетов
        self.specprior.load()
        self.specprior.show()

    def univpr(self):  # Загрузка окна приоритетов университетов
        self.univprior.load()
        self.univprior.show()

    def set_univ(self, i):  # Установка выбранного университета во вторую вкладку главного окна
        self.heading_univ.setText(self.sender().text()[3:])
        univ_id = self.sender().text().split('.')[0]
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
            spec_name = QPushButton()
            label1 = QLabel()
            label2 = QLabel()

            spec_name.setText(self.db.get_name_specialties(i['specialties_code']))
            spec_name.clicked.connect(lambda: self.name_update(univ_id))
            label1.setText(str(i['budget_place']))
            label2.setText(str(i['pass_mark']))
            self.layout1.addWidget(spec_name, x, 0)
            self.layout1.addWidget(label1, x, 1)
            self.layout1.addWidget(label2, x, 2)
            x += 1

    def photo(self): # Сохранение фотографии
        fname = \
            QFileDialog.getOpenFileName(self, 'Выберите изображение', '', 'Изображение (*.png *.xpm *.jpg *.jpeg)')[0]
        if fname != '':
            cop = Image.open(fname)
            cop1 = cop.copy()
            pic = f'img/{self.id}.jpeg'
            cop1.save(pic)
            self.db.set_user_img(self.id, pic)
        pixmap = QPixmap(self.db.find_user_data(self.id)['img']).scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.photoLabel.setPixmap(pixmap)

    def name_update(self, id):  # Загрузка класса со списками учеников на факультете
        if self.sender().text().split('.')[0] == id:
            pass
        else:
            code = self.db.get_code_specialties(self.sender().text())
        self.names.update(id, code)
        self.names.show()

    def special(self):  # Загрузка класса с выбором баллов за ЕГЭ
        self.spec.update()
        self.spec.show()

    def hiding(self, hide):  # Метод для переключения профиля между входом/регистрацией и самим профилем
        elements = [self.photoLabel, self.name_label, self.exitButton, self.editButton,
                    self.login, self.login_label, self.gender, self.gender_label, self.pointsButton, self.facButton,
                    self.vuzButton, self.vuz_label, self.spec_label, self.priorVuz_label, self.priorSpec_label,
                    self.update_button, self.photo_button]
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

    def apply(self, id):  # Метод для установки ранее введеных данных (в других классах)
        self.id = id
        data = self.db.find_user_data(id)
        self.name_label.setText(data['first_name'] + ' ' + data['last_name'])
        if data['gender'] == 'man':
            self.gender.setText('Мужской')
        else:
            self.gender.setText('Женский')
        self.login.setText(data['login'])
        pixmap = QPixmap(data['img']).scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.photoLabel.setPixmap(pixmap)
        self.priorUpdate(self.id)
        self.hiding(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Profile()
    ex.show()
    sys.exit(app.exec_())
