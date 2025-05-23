from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def finish_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_reply_markup(
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Начать тест", callback_data="start_test")]
        ])
    )