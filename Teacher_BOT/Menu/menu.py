from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CallbackContext
)



async def menu(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Хочу учиться", callback_data='menu_button_teacher')],
        [InlineKeyboardButton("Помощь", callback_data='menu_button_help')],
        [InlineKeyboardButton("Остановить бота", callback_data='menu_button_stop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        query = update.callback_query
        await query.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return ConversationHandler.END