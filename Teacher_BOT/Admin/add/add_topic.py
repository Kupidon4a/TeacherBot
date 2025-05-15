from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

#Добавление темы
async def add_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    try:
        args = shlex.split(update.message.text)[1:]
    except ValueError:
        await update.message.reply_text("⚠️ Ошибка в формате команды.")
        return

    if not context.args or len(args) != 3:
        await update.effective_message.reply_text('✏️ Использование команды: /add_topic "Название дисциплины" "Название курса" "Название темы"')
        return
    print(args)

    discipline, course, new_topic = args
    if db.is_topic(discipline, course, new_topic):
        await update.effective_message.reply_text(f"❌ Тема {new_topic} уже существует!")
    else:
        if not db.is_discipline(discipline):
            await update.effective_message.reply_text(f"❌ Дисциплина {discipline} не существует!")
        elif not db.is_course(discipline, course):
            await update.effective_message.reply_text(f"❌ Курс {course} не существует!")
        else:
            db.add_topic(discipline, course, new_topic)
            await update.effective_message.reply_text(f"✅ Тема {new_topic} успешно добавлена!")