from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

import shlex
   
#Удаление урока
async def del_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.effective_message.reply_text('✏️ Использование команды: /del_lesson "Название дисциплины" "Название курса" "Название темы" "Название урока"')
        return
    print(args)

    discipline, course, topic, delete_lesson_title = args
    if db.is_lesson(discipline, course, topic, delete_lesson_title) and db.is_topic(discipline, course, topic) and db.is_course(discipline, course) and db.is_discipline(discipline):
        db.del_lesson(discipline, course, topic, delete_lesson_title)
        await update.effective_message.reply_text(f"✅ Тема {delete_lesson_title} успешно удалена!")        
    else:
        await update.effective_message.reply_text(f"❌ Удаляемый урок {delete_lesson_title} не существует в теме {topic} в курсе {course} и в дисциплине {discipline}!")
  