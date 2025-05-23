from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message

#Получение списка дисциплин
async def get_disciplines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username

        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        disciplines = db.admin_get_disciplines()
        print(disciplines)
        if not disciplines:
            await update.effective_message.reply_text("В базе данных нет дисциплин.")
            return
        message = "📊 Список дисциплин:\n\n"
        for i, discipline in enumerate(disciplines, 1):
            
            message += (
                f"{i}. 📘 Дисциплина: {discipline['discipline']}\n\n"
            )
        
        await send_large_message(update, message)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении дисциплин: {str(e)}")