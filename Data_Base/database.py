from pymongo import MongoClient
from config import *
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection_disciplines = self.db[COLLECTION_NAME_DISCIPLINES]
        self.collection_courses = self.db[COLLECTION_NAME_COURSES]
        self.collection_topics = self.db[COLLECTION_NAME_TOPICS]
        self.collection_lessons = self.db[COLLECTION_NAME_LESSONS]
        self.collection_tests = self.db[COLLECTION_NAME_TESTS]
        self.collection_users = self.db[COLLECTION_NAME_USERS]
        self.collection_answers = self.db[COLLECTION_NAME_ANSWERS]

    #Добавление нового пользователя
    def add_user(self, first_name, last_name, age, city, login):
        db.collection_users.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "city": city,
            "login": login,
            "role": "user",
            "datetime": datetime.now()
        })

    #Получение доступных дисциплин для пользователя
    def get_disciplines(self):
        disciplines = self.collection_disciplines.find({}, {"discipline": 1})
        return [discipline["discipline"] for discipline in disciplines]

    #Получение доступных курсов для пользователя
    def get_courses(self, discipline):
        courses = self.collection_courses.find({"discipline": discipline}, {"course": 1})
        return [course["course"] for course in courses]

    #Получение доступных тем для пользователя
    def get_topics(self, discipline, course):
        topics = self.collection_topics.find({"discipline": discipline, "course": course}, {"topic": 1})
        return [topic["topic"] for topic in topics]  
    
    #Получение доступных названий уроков для пользователя
    def get_lessons(self, discipline, course, topic):
        titles = self.collection_lessons.find({"discipline": discipline, "course": course, "topic": topic}, {"title": 1})
        return [title["title"] for title in titles]

    #Получение одного урока для пользователя
    def get_lesson(self, discipline, course, topic, title):
        lesson = self.collection_lessons.find_one({"discipline": discipline, "course": course, "topic": topic, "title": title}, {"lesson": 1})
        return lesson["lesson"] 
    
    #Получение теста для пользователя
    def get_lesson_test(self, discipline, course, topic, title):
        questions = self.collection_tests.find_one({"discipline": discipline, "course": course, "topic": topic, "title": title}, {"_id": 0, "questions": 1})
        return questions.get("questions", []) if questions else []
        

    #Функции, использующиеся в админ-панели

    #Проверка существования пользователя в системе
    def is_user(self, login):
        user = db.collection_users.find_one({"login": login}) 
        print(user)
        if user != None:
            return True
        else:
            return False

    #Получение списка пользователей с информацией о них
    def get_users(self):
        users = self.collection_users.find({}, {})
        return [user for user in users]
    
    #Получение списка всех дисциплин с информацией о них
    def admin_get_disciplines(self):
        disciplines = self.collection_disciplines.find({}, {})
        return [discipline for discipline in disciplines]
    
    #Получение списка всех курсов с полной информацией о них
    def admin_get_courses(self):
        courses = self.collection_courses.find({}, {})
        return [course for course in courses]

    #Получение списка всех тем с полной информацией о них
    def admin_get_topics(self):
        topics = self.collection_topics.find({}, {})
        return [topic for topic in topics]

    #Получение списка всех уроков с полной информацией о них
    def admin_get_lessons(self):
        lessons = self.collection_lessons.find({}, {})
        return [lesson for lesson in lessons]
    
    #Получение списка всех тестов с полной информацией о них
    def get_tests(self):
        tests = self.collection_tests.find({}, {})
        return [test for test in tests]

    #Проверка является ли пользователь администратором
    def is_admin(self, login):
        if db.collection_users.find_one({"login": login, "role": "admin"}) != None:
            return True
        else:
            return False
    
    #Изменение роли с пользователя на администратора
    def add_admin(self, login_admin):
        if self.is_user(login_admin):
            res = self.collection_users.update_one({"login": login_admin}, {"$set": {"role": "admin"}})
            print(res)
            return res
    
    #Изменение роли с администратора на пользователя
    def del_admin(self, login_admin):
        if self.is_user(login_admin):
            res = self.collection_admins.delete_one({"login": login_admin})
            print(res)
            return res
    
    #Удаление пользователя из системы
    def del_user(self, login):
        if db.collection_users.find_one({"login": login}) != None:
            self.collection_users.delete_one({"login": login})

    #Проверка существования указанной дисциплины в системе
    def is_discipline(self, discipline):
        if db.collection_disciplines.find_one({"discipline": discipline}) != None:
            return True#False
        else:
            return False#True
        
    #Добавление новой дисциплины в систему
    def add_discipline(self, discipline):
        res = self.collection_disciplines.insert_one({"discipline": discipline})
        return res

    #Удаление дисциплины из системы
    def del_discipline(self, discipline):
        res = self.collection_disciplines.delete_one({"discipline": discipline})
        return res    
    
    #Проверка существования указанного курса в системе
    def is_course(self, discipline, course):
        if db.collection_courses.find_one({"discipline": discipline, "course": course}) != None:
            return True#False
        else:
            return False#True

    #Добавление нового курса в систему
    def add_course(self, discipline, course):
        res = self.collection_courses.insert_one({"discipline": discipline, "course": course})
        return res

    #Удаление курса из системы
    def del_course(self, discipline, course):
        res = self.collection_courses.delete_one({"discipline": discipline, "course": course})
        return res
    
    #Проверка существования указанной темы в системе
    def is_topic(self, discipline, course, topic):
        if db.collection_topics.find_one({"discipline": discipline, "course": course, "topic": topic}) != None:
            return True#False
        else:
            return False#True

    #Добавление новой темы в систему
    def add_topic(self, discipline, course, topic):
        res = self.collection_topics.insert_one({"discipline": discipline, "course": course, "topic": topic})
        return res

    #Удаление темы из системе
    def del_topic(self, discipline, course, topic):
        res = self.collection_topics.delete_one({"discipline": discipline, "course": course, "topic": topic})
        return res
    
    #Проверка существования урока в системе
    def is_lesson(self, discipline, course, topic, title):
        if db.collection_lessons.find_one({"discipline": discipline, "course": course, "topic": topic, "title": title}):
            return True
        else:
            return False
        
    #Добавление нового урока в систему
    def add_lesson(self, discipline, course, topic, title, text):
        res = self.collection_lessons.insert_one({"discipline": discipline, "course": course, "topic": topic, "title": title, "lesson": text})
        return res
    
    #Удаление урока из системы
    def del_lesson(self, discipline, course, topic, title):
        res = self.collection_lessons.delete_one({"discipline": discipline, "course": course, "topic": topic, "title": title})
        return res
    
    #Проверка существования тестов в системе
    def is_test(self, discipline, course, topic, title):
        if self.collection_tests.find_one({"discipline": discipline, "course": course, "topic": topic, "title": title}):
            return True
        else:
            return False
        
    #Проверка существования теста в системе
    def is_question(self, discipline, course, topic, title, question):
        if self.collection_tests.find_one({"discipline": discipline, "course": course, "topic": topic, "title": title,  "questions.text": question}):
            return True
        else:
            return False
    
    #Добавление нового теста в систему
    def add_test(self, discipline, course, topic, title, type, text, correct_answer, options=None):
        filter_query = {
            "discipline": discipline,
            "course": course,
            "topic": topic,
            "title": title
        }

        question = {
            "type": type,
            "text": text,
            "correct_answer": correct_answer
        }

        if type == "multiple_choice" and options:
            question["options"] = options

        existing_doc = self.collection_tests.find_one(filter_query)

        if existing_doc:
            self.collection_tests.update_one(
                filter_query,
                {"$push": {"questions": question}}
            )
        else:
            new_doc = {
                **filter_query,
                "questions": [question]
            }
            self.collection_tests.insert_one(new_doc)


    #Удаление теста из вопроса.
    def del_test(self, discipline, course, topic, title, question_text):
        try:
            result = self.collection_tests.update_one(
                {
                    "discipline": discipline,
                    "course": course,
                    "topic": topic,
                    "title": title,
                    "questions.text": question_text
                },
                {
                    "$pull": {"questions": {"text": question_text}}
                }
            )
            if result.modified_count > 0:
                return "✅ Тест был успешно удален."
            else:
                return "❌ Не удалось найти тест с такими параметрами."
        except Exception as e:
            return f"Произошла ошибка при удалении теста: {str(e)}" 


    #Добавление результата прохождения теста пользователем
    def add_result_test(self, login, discipline, course, topic, title_lesson, question, user_answer, correct_answer, is_correct_answer):
        res = self.collection_answers.insert_one({"login": login, "discipline": discipline, "course": course, "topic": topic, "title": title_lesson, "question":question, "user_answer": user_answer, "correct_answer": correct_answer, "is_correct": is_correct_answer})
        return res

    #Получение общей статистики по прохождению уроков
    async def get_all_results(self):
        return list(self.collection_answers.find({}))

db = Database()