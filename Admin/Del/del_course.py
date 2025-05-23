from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex
    

#Удаление учебного курса
async def del_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.effective_message.reply_text('✏️ Использование команды: /del_course "Название дисциплины" "Название курса"')
        return
    print(args)

    discipline, delete_course = args
    if not db.is_course(discipline, delete_course):
        await update.effective_message.reply_text(f"❌ Удаляемый курс {delete_course} не существует!")
    else:
        if not db.is_discipline(discipline):
            await update.effective_message.reply_text(f"❌ Дисциплина {discipline} не существует!")
        else:
            db.del_course(discipline, delete_course)
            await update.effective_message.reply_text(f"✅ Курс {delete_course} успешно удален!")

    if db.is_course(discipline, delete_course) and db.is_discipline(discipline):
        db.del_course(discipline, delete_course)
        await update.effective_message.reply_text(f"✅ Курс {delete_course} успешно удален!")        
    else:
        await update.effective_message.reply_text(f"❌ Удаляемый курс {delete_course} не существует в дисциплине {discipline}!")