from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext
)


async def help(update: Update, context: CallbackContext):
    keyboard_help = [
        [InlineKeyboardButton("Смогу ли я устроиться на работу, если буду учиться с тобой?", callback_data='help_button_work')],
        [InlineKeyboardButton("К кому можно обращаться в случае возникновения вопросов?", callback_data='help_button_question')],
        [InlineKeyboardButton("Каким образом можно оставить обратную связь при работе с ботом?", callback_data='help_button_feedback')],
        [InlineKeyboardButton("Возможно ли каким-то образом пропустить опрос по изученным материалам?", callback_data='help_button_survey')],
        [InlineKeyboardButton("Кто является автором всех учебных материалов?", callback_data='help_button_author')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_help)
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text("Выберите вопрос:", reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text("Выберите вопрос:", reply_markup=reply_markup)