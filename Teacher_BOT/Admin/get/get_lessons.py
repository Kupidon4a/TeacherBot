from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message

#Получение списка уроков
async def get_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username

        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        lessons = db.admin_get_lessons()
        
        if not lessons:
            await update.effective_message.reply_text("В базе данных нет курсов.")
            return
        message = "📊 Список уроков:\n\n"
        for i, lesson in enumerate(lessons, 1):
            
            message += (
                f"{i}. 📘 Дисциплина: {lesson['discipline']}\n"
                f"   📗 Курс: {lesson['course']}\n"
                f"   📙 Тема: {lesson['topic']}\n"
                f"   📓 Название урока: {lesson['title']}\n"
                f"   🧪 Текст урока: {lesson['lesson']}\n\n"
            )
        
        await send_large_message(update, message)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении уроков: {str(e)}")