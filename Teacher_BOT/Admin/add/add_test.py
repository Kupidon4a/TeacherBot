from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

#Добавление теста
async def add_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    try:
        args = shlex.split(update.message.text)[1:]
    except ValueError:
        await update.message.reply_text("⚠️ Ошибка в формате команды.")
        return

    if not args or len(args) != 4:
        await update.effective_message.reply_text(
            '✏️ Использование: /add_test "Название дисциплины" "Название курса" "Название темы" "Название урока"'
        )
        return

    discipline, course, topic, lesson = args

    # Проверки существования указанных параметров в системе
    if not db.is_discipline(discipline):
        await update.message.reply_text(f"❌ Дисциплина {discipline} не найдена.")
        return
    if not db.is_course(discipline, course):
        await update.message.reply_text(f"❌ Курс {course} не найден в дисциплине {discipline}.")
        return
    if not db.is_topic(discipline, course, topic):
        await update.message.reply_text(f"❌ Тема {topic} не найдена в курсе {course} и в дисциплине {discipline}.")
        return
    if not db.is_lesson(discipline, course, topic, lesson):
        await update.message.reply_text(f"❌ Урок {lesson} не найден в теме {topic} в курсе {course} и в дисциплине {discipline}.")
        return

    #Сохраняем в context данные
    context.user_data["add_test"] = {
        "discipline": discipline,
        "course": course,
        "topic": topic,
        "lesson": lesson,
        "stage": "ask_question_text",
        "question": {}
    }
    context.user_data["add_lesson_test"] = True
    await update.message.reply_text("❓ Введите текст добавляемого вопроса:")