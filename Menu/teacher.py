from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes
)

from Data_Base.database import db

async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    disciplines = db.get_disciplines()
    
    if not disciplines:
        await query.message.reply_text("Дисциплины не найдены в базе данных.")
        return
    
    buttons = [
        [InlineKeyboardButton(disc, callback_data=f"teacher_disc_{disc}")]
        for disc in disciplines
    ]
    
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="teacher_back")])
    
    await query.message.reply_text(
        "Выбери дисциплину для изучения:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
