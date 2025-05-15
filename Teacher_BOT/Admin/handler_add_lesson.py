from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
    
#Обработчик ввода текста урока
async def handler_add_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data["data_add_lesson_text"]
    lesson_text = update.message.text
    await update.message.reply_text(f"Текст добавленного урока:\n {lesson_text}")
    db.add_lesson(data["discipline"], data["course"], data["topic"], data["lesson"], lesson_text)

    await update.message.reply_text(f"✅ Урок «{data['lesson']}» успешно добавлен!")

    context.user_data["add_lesson_text"] = False
    return