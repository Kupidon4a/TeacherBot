from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message
#Получение списка курсов
async def get_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username

        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        courses = db.admin_get_courses()
        
        if not courses:
            await update.effective_message.reply_text("В базе данных нет курсов.")
            return
        message = "📊 Список курсов:\n\n"
        for i, course in enumerate(courses, 1):
            
            message += (
                f"{i}. 📘 Дисциплина: {course['discipline']}\n"
                f"   📗 Курс: {course['course']}\n\n"
            )
        
        await send_large_message(update, message)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении курсов: {str(e)}")