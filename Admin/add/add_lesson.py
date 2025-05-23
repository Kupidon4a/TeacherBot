from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

    
#Добавление урока и тестов к нему
async def add_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    try:
        args = shlex.split(update.message.text)[1:]
    except ValueError:
        await update.message.reply_text("⚠️ Ошибка в формате команды.")
        return

    if not context.args or len(args) != 4:
        await update.effective_message.reply_text('✏️ Использование команды: /add_lesson "Название дисциплины" "Название курса" "Название темы" "Название урока"')
        return
    print(args)

    discipline, course, topic, new_lesson_title = args
    if db.is_lesson(discipline, course, topic, new_lesson_title):
        await update.effective_message.reply_text(f"❌ Урок {new_lesson_title} уже существует!")
        return
    else:
        if not db.is_discipline(discipline):
            await update.effective_message.reply_text(f"❌ Дисциплина {discipline} не существует!")
            return
        elif not db.is_course(discipline, course):
            await update.effective_message.reply_text(f"❌ Курс {course} не существует!")
            return
        elif not db.is_topic(discipline, course, topic):
            await update.effective_message.reply_text(f"❌ Тема {topic} не существует!")
            return

    # Устанавливаем ожидание текста
    context.user_data["data_add_lesson_text"] = {
        "discipline": discipline,
        "course": course,
        "topic": topic,
        "lesson": new_lesson_title
    }

    await update.message.reply_text(
        f"✍️ Введите текст урока для «{new_lesson_title}».\n"
        "Если хотите разбить его на части, используйте два пробела подряд."
    )
    context.user_data["add_lesson_text"] = True