from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message

#Получение списка пользователей   
async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username

        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        users = db.get_users()
        
        if not users:
            await update.effective_message.reply_text("В базе данных нет пользователей.")
            return
        message = "📊 Список пользователей:\n\n"
        for i, user in enumerate(users, 1):
            reg_date = user['datetime'].strftime("%d.%m.%Y %H:%M") if user['datetime'] else "не указана"
            message += (
                f"👤 {i}. {user['first_name']} {user['last_name']}\n"
                f"   ▪️ Возраст: {user['age']}\n"
                f"   ▪️ Город: {user['city']}\n"
                f"   ▪️ Telegram: @{user['login']}\n"
                f"   ▪️ Роль: {user['role']}\n"
                f"   ▪️ Дата регистрации: {reg_date}\n\n"
            )
        
        await send_large_message(update, message)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении пользователей: {str(e)}")