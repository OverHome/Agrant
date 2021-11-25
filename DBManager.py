import sqlite3
import hashlib
import operator


class DBManager:

    def __init__(self):
        self.user_title = ["id", "login", "password", "first_name", "last_name", "gender"]
        self.USE_title = ["id", "russian_language", "mathematics", "physics", "chemistry", "history", "social_studies",
                          "ICT", "biology", "geography", "foreign_languages", "literature"]

        self.universities_title = ["id", "name", "city", "average_USE"]
        self.universities_specialties_title = ["id", "universities_id", "specialties_code", "budget_place", "pass_mark"]

        self.conn = sqlite3.connect("agrant.db")
        self.cur = self.conn.cursor()

    def add_user(self, login, password, fname, lname,  gender):
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

    def add_user_USE(self, login):
        user_line = self.find_user_line(login)
        sql_req = f"""
        INSERT INTO USE
        (id)
        VALUES({user_line["id"]})
        """
        self.cur.execute(sql_req)
        self.conn.commit()

    def in_base(self, login):
        sql_req = f"""SELECT * 
        FROM users 
        WHERE login = '{login.lower()}'
        """
        return bool(len(list(self.cur.execute(sql_req))))

    def sing_in(self, login, password):
        if self.in_base(login):
            user_line = self.find_user_line(login)
            pas_hex = self.hesh(password)
            if user_line["password"] == pas_hex:
                return user_line["id"]
            else:
                return "Неверный пароль"
        else:
            return "Пользователя не существует"

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

    def is_user(self, login, fname, lname):
        if self.in_base(login):
            user_line = self.find_user_line(login)
            if user_line["first_name"] == fname.capitalize() and user_line["last_name"] == lname.capitalize():
                return "Пользователь подтвержден"
            else:
                return "Пользователь не подтвержден"
        else:
            return "Пользователя не существует"

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

    @staticmethod
    def hesh(password):
        return hashlib.sha1(bytes(password, encoding="UTF-8")).hexdigest()
