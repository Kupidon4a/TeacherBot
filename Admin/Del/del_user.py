from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

# Удаление данных о пользователе бота
async def del_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username

    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    if not context.args or len(context.args) != 1:
        await update.effective_message.reply_text('✏️ Использование: /add_admin @Логин')
        return

    del_user = context.args[0].lstrip("@")
    if db.is_user(del_user):
        db.del_user(del_user)
        await update.effective_message.reply_text(f"✅ Пользователь @{del_user} удален из списка пользователей.")
    else:
        await update.effective_message.reply_text(f"❌ Пользователь @{del_user} не cуществует в базе данных!")