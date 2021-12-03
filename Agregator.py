import threading
from DBManager import DBManager


class Agregator:

    def __init__(self):
        self.lessons = {1: "russian_language",
                        2: "mathematics",
                        3: "physics",
                        4: "chemistry",
                        5: "history",
                        6: "social_studies",
                        7: "ICT",
                        8: "biology",
                        9: "geography",
                        10: "foreign_languages",
                        11: "literature",
                        12: "achievements"}
        self.in_progress = False

    def set_data(self):
        self.db = DBManager()
        self.users_id = self.db.get_all_user_id()
        self.users_USE = self.db.get_all_USE()
        self.users_prioritets = self.db.get_all_priorities()
        self.universities_specialties_budget_place = self.db.get_all_budget_place()
        self.subjects, self.subjects_of_choice = self.db.get_all_specialties_lesson()

    def sum_USE(self, user, specialties_id):
        sm = 0
        for i in self.subjects[specialties_id]:
            sm += self.users_USE[user][self.lessons[i]]
        mx = 0

        if specialties_id in self.subjects_of_choice:
            for i in self.subjects_of_choice[specialties_id]:
                mx = max(mx, self.users_USE[user][self.lessons[i]])

        sm += mx + self.users_USE[user][self.lessons[12]]
        return sm

    def start_distribution(self):
        if not self.in_progress:
            self.in_progress = True
            thread_distribution = threading.Thread(target=self.distribution)
            thread_distribution.start()

    def distribution(self):
        self.set_data()
        specialties_users = {}
        specialties_keys = list(self.universities_specialties_budget_place.keys())
        for i in specialties_keys:
            specialties_users[i] = []

        for user in self.users_id:
            if user in self.users_prioritets:
                specialties = self.users_prioritets[user][0]
                USE = self.sum_USE(user, specialties)
                specialties_users[specialties] += [(user, USE)]
                specialties_users[specialties].sort(key=lambda x: (x[1]), reverse=True)
        tlen = 1
        ln = 0
        failed_user = []
        failed_user_temp = []
        while tlen != ln:
            tlen = ln
            for key in range(len(specialties_keys)):
                failed_user = failed_user_temp
                failed_user_temp = []
                for i in specialties_keys:
                    while len(specialties_users[i]) > self.universities_specialties_budget_place[i]:
                        user_data = specialties_users[i].pop(-1)
                        failed_user += [user_data[0]]

                for user in failed_user:
                    if user in self.users_prioritets and len(self.users_prioritets[user]) > key:
                        specialties = self.users_prioritets[user][key]
                        USE = self.sum_USE(user, specialties)
                        specialties_users[specialties] += [(user, USE)]
                        specialties_users[specialties].sort(key=lambda x: (x[1]), reverse=True)
                    else:
                        failed_user_temp += [user]
            ln = len(failed_user)
        self.db.set_enlisted_user(specialties_users)
        self.in_progress = False
