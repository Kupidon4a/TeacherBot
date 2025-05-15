from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

#Добавление нового администратора
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    if not context.args or len(context.args) != 1:
        await update.effective_message.reply_text("✏️ Использование: /add_admin @Логин")
        return

    new_admin = context.args[0].lstrip("@")
    
    if db.is_admin(new_admin):
        await update.effective_message.reply_text(f"❌ Пользователь @{new_admin} уже итак администратор!")
    else:
        if db.is_user(new_admin):
            db.add_admin(new_admin)
            await update.effective_message.reply_text(f"✅ Пользователь @{new_admin} добавлен в список админов.")
        else:
            await update.effective_message.reply_text(f"❌ Пользователь @{new_admin} не зарегистрирован в боте.")
