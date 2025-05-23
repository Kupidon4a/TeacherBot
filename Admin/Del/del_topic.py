from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex
    
#Удаление темы
async def del_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.effective_message.reply_text('✏️ Использование команды: /del_topic "Название дисциплины" "Название курса" "Название темы"')
        return
    print(args)

    discipline, course, delete_topic = args
    if db.is_topic(discipline, course, delete_topic) and db.is_course(discipline, course) and db.is_discipline(discipline):
        db.del_topic(discipline, course, delete_topic)
        await update.effective_message.reply_text(f"✅ Тема {delete_topic} успешно удалена!")        
    else:
        await update.effective_message.reply_text(f"❌ Удаляемая тема {delete_topic} не существует в курсе {course} и в дисциплине {discipline}!")