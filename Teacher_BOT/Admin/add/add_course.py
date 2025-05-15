from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

   
#Добавление учебного курса
async def add_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    try:
        args = shlex.split(update.message.text)[1:]
    except ValueError:
        await update.message.reply_text("⚠️ Ошибка в формате команды.")
        return

    if not context.args or len(args) != 2:
        await update.effective_message.reply_text('✏️ Использование команды: /add_course "Название дисциплины" "Название курса"')
        return
    print(context.args)

    discipline, new_course = args
    if db.is_course(discipline, new_course):
        await update.effective_message.reply_text(f"❌ Курс {new_course} уже существует!")
    else:
        if not db.is_discipline(discipline):
            await update.effective_message.reply_text(f"❌ Дисциплина {discipline} не существует!")
        else:
            db.add_course(discipline, new_course)
            await update.effective_message.reply_text(f"✅ Курс {new_course} успешно добавлен!")