from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message

#Получение списка тем
async def get_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username

        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        topics = db.admin_get_topics()
        
        if not topics:
            await update.effective_message.reply_text("В базе данных нет курсов.")
            return
        message = "📊 Список тем:\n\n"
        for i, topic in enumerate(topics, 1):
            
            message += (
                f"{i}. 📘 Дисциплина: {topic['discipline']}\n"
                f"   📗 Курс: {topic['course']}\n"
                f"   📙 Тема: {topic['topic']}\n\n"
            )
        
        await send_large_message(update, message)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении тем: {str(e)}")