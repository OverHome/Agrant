import sqlite3
import hashlib
import operator


class DBManager:
    # Инициализация объекта класса взаимодействующего с базой данных
    def __init__(self):
        # Константы заголовков для возвращения
        self.user_title = ["id", "login", "password", "first_name", "last_name", "gender", "img"]
        self.USE_title = ["id", "russian_language", "mathematics", "physics", "chemistry", "history", "social_studies",
                          "ICT", "biology", "geography", "foreign_languages", "literature", "achievements"]

        self.universities_title = ["id", "name", "city", "average_USE", "logo"]
        self.universities_specialties_title = ["id", "universities_id", "specialties_code", "budget_place", "pass_mark"]
        self.priorities_title = ["user_id", "un_sp_id", "prioritet"]
        self.specialties_priorities_title = ["id", "user_id", "specialties", "priorities"]
        self.universities_priorities_title = ["id", "user_id", "university", "priorities"]

        self.conn = sqlite3.connect("Database/agrant.db")
        self.cur = self.conn.cursor()

    # Метод добавления пользователя в баззу
    def add_user(self, login, password, fname, lname, gender):
        if not self.in_base(login):
            pas_hex = self.hesh(password)
            user_data = (login.lower(), pas_hex, fname.capitalize(), lname.capitalize(), gender)
            sql_req = f"""
            INSERT INTO users 
            ('login', 'password', 'first_name', 'last_name', 'gender') 
            VALUES(?, ?, ?, ?, ? );
            """
            self.cur.execute(sql_req, user_data)
            self.conn.commit()

            self.add_user_USE(login)
            return "Пользователь создан"
        else:
            return "Имя пользователя занято"

    # Метод инициализация пользовательских данных о сданных ЕГЭ
    def add_user_USE(self, login):
        user_line = self.find_user_line(login)
        sql_req = f"""
        INSERT INTO USE
        (id)
        VALUES({user_line["id"]})
        """
        self.cur.execute(sql_req)
        self.conn.commit()

    # Метод проверки налиция больщователя в базе
    def in_base(self, login):
        sql_req = f"""SELECT * 
        FROM users 
        WHERE login = '{login.lower()}'
        """
        return bool(len(list(self.cur.execute(sql_req))))

    # Метод входа в учетную запись
    def sign_in(self, login, password):
        if self.in_base(login):
            user_line = self.find_user_line(login)
            pas_hex = self.hesh(password)
            if user_line["password"] == pas_hex:
                return user_line["id"]
            else:
                return "Неверный пароль"
        else:
            return "Пользователя не существует"

    # Метод нахождения даннхы пользователя в базе по логину
    def find_user_line(self, login):
        user_dict = {}
        sql_req = f"""
        SELECT * 
        FROM users 
        WHERE login = '{login.lower()}'
        """
        user_line = list(self.cur.execute(sql_req))[0]
        for i in range(len(self.user_title)):
            user_dict[self.user_title[i]] = user_line[i]
        return user_dict

    # Метод нахождения даннхы пользователя в базе по id
    def find_user_data(self, id):
        user_dict = {}
        sql_req = f"""
        SELECT * 
        FROM users 
        WHERE id = '{id}'
        """
        user_line = list(self.cur.execute(sql_req))[0]
        for i in range(len(self.user_title)):
            user_dict[self.user_title[i]] = user_line[i]
        return user_dict

    # Метод проверки валидности введенных данных
    def is_user(self, login, fname, lname):
        if self.in_base(login):
            user_line = self.find_user_line(login)
            if user_line["first_name"] == fname.capitalize() and user_line["last_name"] == lname.capitalize():
                return "Пользователь подтвержден"
            else:
                return "Пользователь не подтвержден"
        else:
            return "Пользователя не существует"

    # Метод смены пароля
    def change_password(self, login, password):
        if self.in_base(login):
            pas_hex = self.hesh(password)
            sql_req = f"""
            UPDATE users 
            SET password = '{pas_hex}' 
            WHERE login = '{login.lower()}'
            """
            self.cur.execute(sql_req)
            self.conn.commit()
            return "Пароль изменен"
        else:
            return "Пользователя не существует"

    # Метод изменения пользовательсикх данных
    def change_user_data(self, login, fname, lname, gender):
        if self.in_base(login):
            sql_req = f"""
            UPDATE users 
            SET first_name = '{fname}',
            last_name = '{lname}',
            gender = '{gender}'
            WHERE login = '{login.lower()}'
            """
            self.cur.execute(sql_req)
            self.conn.commit()
            return "Данные акаунта изменены"
        else:
            return "Пользователя не существует"

    # Метод изменения данных ЕГЭ у пользователя
    def set_USE_points(self, id, points):
        sql_req = f"""
        UPDATE USE
        set russian_language='{points["russian_language"]}',
        mathematics='{points["mathematics"]}',
        physics='{points["physics"]}',
        chemistry='{points["chemistry"]}',
        history='{points["history"]}',
        social_studies='{points["social_studies"]}',
        ICT='{points["ICT"]}',
        biology='{points["biology"]}',
        geography='{points["geography"]}',
        foreign_languages='{points["foreign_languages"]}',
        literature='{points["literature"]}',
        achievements='{points["achievements"]}'
        WHERE id = '{id}'
        """
        self.cur.execute(sql_req, points)
        self.conn.commit()
        self.set_user_priorities(id)

    # Метод установки приоритетов вузов
    def set_universities_priorities(self, user_id, universities_priorities):
        sql_req = f"""
                DELETE
                FROM user_priorities_un
                WHERE user_id ={user_id} 
                """
        self.cur.execute(sql_req)
        self.conn.commit()

        sql_req = f"""
                INSERT INTO user_priorities_un 
                ('user_id', 'university', 'priorities') 
                VALUES(?, ?, ?);
                """
        for i in range(len(universities_priorities)):
            self.cur.execute(sql_req, (user_id, universities_priorities[i], i))
            self.conn.commit()
        self.set_user_priorities(user_id)

    # Метод установки приоритетов специальностей
    def set_specialties_priorities(self, user_id, specialties_priorities):
        sql_req = f"""
                DELETE
                FROM user_priorities_sp
                WHERE user_id ={user_id} 
                """
        self.cur.execute(sql_req)
        self.conn.commit()

        sql_req = f"""
                INSERT INTO user_priorities_sp
                ('user_id', 'specialties', 'priorities') 
                VALUES(?, ?, ?);
                """
        for i in range(len(specialties_priorities)):
            self.cur.execute(sql_req, (user_id, specialties_priorities[i], i))
            self.conn.commit()
        self.set_user_priorities(user_id)

    # Метод получения приоритетов вузов
    def get_universities_priorities(self, user_id):
        universities_priorities = []
        sql_req = f"""
                SELECT * 
                FROM user_priorities_un
                WHERE user_id = {user_id}
                       """
        universities_priorities_lines = list(self.cur.execute(sql_req))
        for line in universities_priorities_lines:
            res = {}
            for i in range(len(self.universities_priorities_title)):
                res[self.universities_priorities_title[i]] = line[i]
            universities_priorities += [res]
        return universities_priorities

    # Метод получения приоритетов специальностей
    def get_specialties_priorities(self, user_id):
        specialties_priorities = []
        sql_req = f"""
                SELECT * 
                FROM user_priorities_sp
                WHERE user_id = {user_id}
                       """
        specialties_priorities_lines = list(self.cur.execute(sql_req))
        for line in specialties_priorities_lines:
            res = {}
            for i in range(len(self.specialties_priorities_title)):
                res[self.specialties_priorities_title[i]] = line[i]
            specialties_priorities += [res]
        return specialties_priorities

    # Метод получения данных ЕГЭ у пользователя
    def get_USE_points(self, id):
        user_dict = {}
        sql_req = f"""
                SELECT * 
                FROM USE
                WHERE id = '{id}'
                """
        user_line = list(self.cur.execute(sql_req))[0]
        for i in range(len(self.USE_title)):
            user_dict[self.USE_title[i]] = user_line[i]
        return user_dict

    # Метод получения всех университетов
    def get_universities(self):
        universities_array = []
        sql_req = f"""
                SELECT * 
                FROM universities
                """
        universities_lines = list(self.cur.execute(sql_req))

        for university in range(len(universities_lines)):
            university_dict = {}
            for i in range(len(self.universities_title)):
                university_dict[self.universities_title[i]] = universities_lines[university][i]
            universities_array.append(university_dict)
        return universities_array

    # Метод получения всех специальностей в университете
    def get_specialties_in_university(self, un_id):
        specialties_array = []
        sql_req = f"""
                SELECT * 
                FROM universities_specialties
                WHERE un_id = '{un_id}'
                """
        specialties_lines = list(self.cur.execute(sql_req))

        for specialty in range(len(specialties_lines)):
            specialty_dict = {}
            for i in range(len(self.universities_specialties_title)):
                specialty_dict[self.universities_specialties_title[i]] = specialties_lines[specialty][i]
            specialties_array.append(specialty_dict)
        specialties_array.sort(key=operator.itemgetter("specialties_code"))
        return specialties_array

    # Метод получения имени университета
    def get_university_name(self, un_id):
        sql_req = f"""
                        SELECT * 
                        FROM universities
                        WHERE id = '{un_id}'
                        """
        university_name = list(self.cur.execute(sql_req))[0][1]
        return university_name

    # Метод получения всех специальностей
    def get_specialties(self):
        sql_req = f"""
                SELECT * 
                FROM specialties
                """
        specialties_lines = list(self.cur.execute(sql_req))
        return specialties_lines

    # Метод установки пользовательских приоритетов
    def set_user_priorities(self, user_id):
        priorities = []
        sql_req = f"""
                SELECT * 
                FROM user_priorities_sp
                WHERE user_id = {user_id}
                """
        user_priorities_sp = list(self.cur.execute(sql_req))

        sql_req = f"""
                SELECT * 
                FROM user_priorities_un
                WHERE user_id = {user_id}
                """
        user_priorities_un = list(self.cur.execute(sql_req))
        k = 0
        for university in user_priorities_un:
            for specialties in user_priorities_sp:

                sql_req = f"""
                        SELECT * 
                        FROM universities_specialties
                        WHERE un_id = {university[2]}
                        AND code = '{specialties[2]}'
                        """
                combo = list(self.cur.execute(sql_req))
                if len(combo) > 0:
                    priorities += [(user_id, combo[0][0], k)]
                    k += 1

        sql_req = f"""
                        DELETE
                        FROM priorities_cash
                        WHERE user_id = {user_id}
                        """
        self.cur.execute(sql_req)
        self.conn.commit()

        for prioritet in priorities:
            sql_req = f"""
                    INSERT INTO priorities_cash 
                    ('user_id', 'un_sp_id', 'prioritet') 
                    VALUES(?, ?, ?);
                    """
            self.cur.execute(sql_req, prioritet)
            self.conn.commit()

    # Метод установки все пользовательских приоритетов (для заполнения пустой базы)
    def set_all_priorities(self):
        priorities = []
        sql_req = f"""
                        SELECT * 
                        FROM users
                        """

        user_lins = list(self.cur.execute(sql_req))
        for user in user_lins:
            k = 1
            sql_req = f"""
                    SELECT * 
                    FROM user_priorities_sp
                    WHERE user_id = {user[0]}
                    """
            user_priorities_sp = list(self.cur.execute(sql_req))

            sql_req = f"""
                    SELECT * 
                    FROM user_priorities_un
                    WHERE user_id = {user[0]}
                    """
            user_priorities_un = list(self.cur.execute(sql_req))

            for university in user_priorities_un:
                for specialties in user_priorities_sp:
                    sql_req = f"""
                            SELECT * 
                            FROM universities_specialties
                            WHERE un_id = {university[2]}
                            AND code = '{specialties[2]}'
                            """
                    combo = list(self.cur.execute(sql_req))
                    if len(combo) > 0:
                        priorities += [(user[0], combo[0][0], k)]
                        k += 1
        for prioritet in priorities:
            sql_req = f"""
                        INSERT INTO priorities_cash 
                        ('user_id', 'un_sp_id', 'prioritet') 
                        VALUES(?, ?, ?);
                        """
            self.cur.execute(sql_req, prioritet)
            self.conn.commit()

    # Метод получения всех пользовательсикх приортитетов
    def get_all_priorities(self):
        user_priorite = {}
        sql_req = f"""
                SELECT * 
                FROM priorities_cash
                """
        priorities = list(self.cur.execute(sql_req))
        for line in priorities:
            if line[0] in user_priorite:
                user_priorite[line[0]] += [line[1]]
            else:
                user_priorite[line[0]] = [line[1]]
        return user_priorite

    # Метод получения всех пользовательсикх данных ЕГЭ
    def get_all_USE(self):
        result = {}
        sql_req = f"""
                SELECT * 
                FROM USE
                """
        user_line = list(self.cur.execute(sql_req))
        for user in range(len(user_line)):
            user_dict = {}
            for i in range(len(self.USE_title)):
                if i == 0:
                    continue
                user_dict[self.USE_title[i]] = user_line[user][i]
            result[user_line[user][0]] = user_dict
        return result

    # Метод получения всех пользовательей
    def get_all_user_id(self):
        result = []
        sql_req = f"""
                SELECT * 
                FROM USE
                """
        user_lines = list(self.cur.execute(sql_req))
        for user in user_lines:
            result.append(user[0])
        return result

    # Метод получения всех бюджетных мест
    def get_all_budget_place(self):
        result = {}
        sql_req = f"""
                SELECT * 
                FROM  universities_specialties
                """
        universities_specialties = list(self.cur.execute(sql_req))
        for line in universities_specialties:
            result[line[0]] = line[3]

        return result

    # Метод получения данных о предметах ЕГЭ для каждого профиля
    def get_all_specialties_lesson(self):
        subjects = {}
        subjects_of_choice = {}
        sql_req = f"""
                SELECT * 
                FROM  specialties_lesson
                """
        specialties_lesson = list(self.cur.execute(sql_req))
        for line in specialties_lesson:
            if line[3] == 1:
                if line[1] not in subjects:
                    subjects[line[1]] = [line[2]]
                else:
                    subjects[line[1]] += [line[2]]
            else:
                if line[1] not in subjects_of_choice:
                    subjects_of_choice[line[1]] = [line[2]]
                else:
                    subjects_of_choice[line[1]] += [line[2]]
        return subjects, subjects_of_choice

    # Метод получения названия специальности по коду
    def get_name_specialties(self, code):
        sql_req = f"""
                SELECT * 
                FROM specialties
                WHERE code = '{code}'
                """
        specialties = list(self.cur.execute(sql_req))[0]
        return specialties[1]

    # Метод получения кода специальности по названию
    def get_code_specialties(self, name):
        sql_req = f"""
                SELECT * 
                FROM specialties
                WHERE name = '{name}'
                """
        specialties = list(self.cur.execute(sql_req))[0]
        return specialties[0]

    # Метод установки данных о поступающих
    def set_enlisted_user(self, specialties_users):
        users_data = []
        sql_req = f"""
                DELETE
                FROM enlisted_user
                """
        self.cur.execute(sql_req)
        self.conn.commit()

        for specialtie in specialties_users:
            for data in specialties_users[specialtie]:
                users_data.append((specialtie, data[0], data[1]))
        sql_req = f"""
                INSERT INTO enlisted_user 
                ('id', 'user_id', 'points') 
                VALUES(?, ?, ?);
                """
        self.cur.executemany(sql_req, users_data)
        self.conn.commit()

    # Метод получения данных о поступающих в вузе по специальности
    def get_enlisted_user(self, un_id, code):
        enlisted_user = []
        sql_req = f"""
                SELECT * 
                FROM universities_specialties
                WHERE un_id = {un_id}
                AND code = '{code}'
                """
        enlisted_user_id = list(self.cur.execute(sql_req))[0][0]
        sql_req = f"""
                       SELECT * 
                       FROM enlisted_user
                       WHERE id = {enlisted_user_id}
                       """
        enlisted_users = list(self.cur.execute(sql_req))
        k = 1
        for line in enlisted_users:
            sql_req = f"""
                    SELECT * 
                    FROM users
                    WHERE id = {line[1]}
                    """
            user_line = list(self.cur.execute(sql_req))[0]
            fname = user_line[3]
            lname = user_line[4]
            enlisted_user.append({"id": k, "fname": fname, "lname": lname, "points": line[2]})
            k += 1
        return enlisted_user

    # Метод установки данных по поступающих
    def get_lessons(self, un_id, code):
        lessons_necessarily = []
        lessons_choice = []
        sql_req = f"""
                SELECT * 
                FROM universities_specialties
                WHERE code = '{code}'
                AND un_id = {un_id}
                """
        specialties_id = list(self.cur.execute(sql_req))[0][0]

        sql_req = f"""
                SELECT * 
                FROM specialties_lesson
                WHERE un_sp_id = {specialties_id}
                """
        lessons_line = list(self.cur.execute(sql_req))
        for lesson in lessons_line:
            sql_req = f"""
                            SELECT * 
                            FROM lesson
                            WHERE id = {lesson[2]}
                            """
            if lesson[3] == 1:
                lessons_necessarily += [list(self.cur.execute(sql_req))[0][2]]
            else:
                lessons_choice += [list(self.cur.execute(sql_req))[0][2]]
        return lessons_necessarily, lessons_choice

    # Метод получения данных пользователя по определению
    def get_distributed_user(self, user_id):
        try:
            sql_req = f"""
                    SELECT * 
                    FROM enlisted_user
                    WHERE user_id = {user_id}
                    """
            enlisted_user_id = list(self.cur.execute(sql_req))[0][0]
            sql_req = f"""
                    SELECT * 
                    FROM universities_specialties
                    WHERE id = {enlisted_user_id}
                    """
            specialties_lesson_line = list(self.cur.execute(sql_req))[0]
            un = self.get_university_name(specialties_lesson_line[1])
            spes = self.get_name_specialties(specialties_lesson_line[2])

            return un, spes
        except:
            return ("Нет", "Нет")

    # Метод сохраниения картинки в бд
    def set_user_img(self, user_id, title):
        sql_req = f"""
                UPDATE users 
                SET img = '{title}'
                WHERE id = '{user_id}'
                """
        self.cur.execute(sql_req)
        self.conn.commit()

    # Метод хеширования пароля
    @staticmethod
    def hesh(password):
        return hashlib.sha1(bytes(password, encoding="UTF-8")).hexdigest()
