import Data_Base.database as db

a = db.db.get_disciplines()

print(a)

b = db.db.get_courses(a[0])
print(b)

c = db.db.get_topics(a[0], b[0])
print(c)

print(a[0])
print(b[0])
print(c[0])
d = db.db.get_lessons(a[0], b[0], c[0])
print(d)
f = db.db.get_lesson(a[0], b[0], c[0], d[0])
print(f)