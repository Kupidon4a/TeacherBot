from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

#Добавление учебной дисциплины
async def add_discipline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    try:
        args = shlex.split(update.message.text)[1:]
    except ValueError:
        await update.message.reply_text("⚠️ Ошибка в формате команды.")
        return

    if not context.args or len(args) != 1:
        await update.effective_message.reply_text('✏️ Использование команды: /add_discipline "Название дисциплины"')
        return
    print(args)

    new_discipline = args[0]
    if db.is_discipline(new_discipline):
        await update.effective_message.reply_text(f"❌ Дисциплина {new_discipline} уже существует!")
    else:
        db.add_discipline(new_discipline)
        await update.effective_message.reply_text(f"✅ Дисциплина {new_discipline} успешно добавлена!")