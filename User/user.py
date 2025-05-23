class User:
    def __init__(self):
        self.login = None
        self.first_name = None
        self.last_name = None
        self.age = None
        self.city = None

        self.discipline = None
        self.topic = None
        self.course = None
        self.lesson = None

        self.title = None


    def set_login(self, login):
        self.login = login

    def get_login(self):
        return self.login

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_last_name(self):
        return self.last_name

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city

    def set_discipline(self, discipline):
        self.discipline = discipline
    
    def set_topic(self, topic):
        self.topic = topic

    def set_course(self, course):
        self.course = course
    
    def set_lesson(self, lesson):
        self.lesson = lesson

    def set_title(self, title):
        self.title = title

    def get_discipline(self):
        return self.discipline
    
    def get_course(self):
        return self.course
    
    def get_topic(self):
        return self.topic

    def get_lesson(self):
        return self.lesson
    
    def get_title(self):
        return self.title

    def clear(self):
        self.discipline = None
        self.course = None
        self.topic = None
        self.lesson = None
        self.title = None

user = User()
























