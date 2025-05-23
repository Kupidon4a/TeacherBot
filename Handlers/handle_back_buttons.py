from telegram import Update
from telegram.ext import ContextTypes

from User.user import user
from Courses.show_courses import show_courses
from Topics.show_topics import show_topics
from Lesson.show_lessons import show_lessons
from Menu.teacher import teacher
from Menu.menu import menu

async def handle_back_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "teacher_back":
        user.set_discipline(None)
        await menu(update, context)

    elif query.data == "back_to_disciplines":
        # Возврат к выбору дисциплины
        user.set_course(None)
        await teacher(update, context)
    
    elif query.data == "back_to_courses":
        # Возврат к выбору курса
        user.set_topic(None)
        await show_courses(update, context)
    
    elif query.data == "back_to_topics":
        # Возврат к выбору темы
        user.set_lesson(None)
        user.set_title(None)
        await show_topics(update, context)

    elif query.data == "back_to_lessons":
        #Возврат к выбору урока
        user.set_lesson(None)
        user.set_title(None)
        await show_lessons(update, context)