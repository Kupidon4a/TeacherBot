from telegram import Update
from telegram.ext import(
    ConversationHandler,
    ContextTypes
)
from User.user import user

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    context.user_data.clear()
    user.clear()
    await message.reply_text("Бот остановлен. Для перезапуска отправьте команду /start")
    if update.callback_query:
        await update.callback_query.answer()
    return ConversationHandler.END