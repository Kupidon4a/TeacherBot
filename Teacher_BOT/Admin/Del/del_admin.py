from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

# Удаление администратора
async def del_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    if not context.args or len(context.args) != 1:
        await update.effective_message.reply_text("✏️ Использование: /del_admin @Логин")
        return

    del_admin = context.args[0].lstrip("@")
    if db.is_admin(del_admin):
        db.del_admin(del_admin)
        await update.effective_message.reply_text(f"✅ Пользователь @{del_admin} удален из списока админов.")
    else:
        await update.effective_message.reply_text(f"❌ Пользователь @{del_admin} не является администратором!")