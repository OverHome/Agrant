import sqlite3
import hashlib
import operator


class DBManager:

    def __init__(self):
        self.user_title = ["id", "login", "password", "first_name", "last_name", "gender"]
        self.USE_title = ["id", "russian_language", "mathematics", "physics", "chemistry", "history", "social_studies",
                          "ICT", "biology", "geography", "foreign_languages", "literature", "achievements"]

        self.universities_title = ["id", "name", "city", "average_USE", "logo"]
        self.universities_specialties_title = ["id", "universities_id", "specialties_code", "budget_place", "pass_mark"]
        self.priorities_title = ["user_id", "un_sp_id", "prioritet"]

        self.conn = sqlite3.connect("agrant.db")
        self.cur = self.conn.cursor()

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

    def get_specialties(self):
        sql_req = f"""
                SELECT * 
                FROM specialties
                """
        specialties_lines = list(self.cur.execute(sql_req))
        return specialties_lines

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
                        k+=1
        for prioritet in priorities:
            sql_req = f"""
                        INSERT INTO priorities_cash 
                        ('user_id', 'un_sp_id', 'prioritet') 
                        VALUES(?, ?, ?);
                        """
            self.cur.execute(sql_req, prioritet)
            self.conn.commit()

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

    def get_name_specialties(self, code):
        sql_req = f"""
                SELECT * 
                FROM specialties
                WHERE code = '{code}'
                """
        specialties = list(self.cur.execute(sql_req))[0]
        return specialties[1]

    @staticmethod
    def hesh(password):
        return hashlib.sha1(bytes(password, encoding="UTF-8")).hexdigest()
