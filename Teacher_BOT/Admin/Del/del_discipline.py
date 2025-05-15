from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex

#Удаление учебной дисциплины
async def del_discipline(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.effective_message.reply_text('✏️ Использование команды: /del_discipline "Название дисциплины"')
        return
    print(context.args)

    del_discipline = args[0]
    if db.is_discipline(del_discipline):
        db.del_discipline(del_discipline)
        await update.effective_message.reply_text(f"✅ Дисциплина {del_discipline} успешно удалена!")
    else:
        await update.effective_message.reply_text(f"❌ Удаляемая дисциплина {del_discipline} не существует!")
  