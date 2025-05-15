from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from Data_Base.database import db
from User.user import user

async def show_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        lessons = db.get_lessons(
            user.get_discipline(),
            user.get_course(),
            user.get_topic()
        )
        
        if not lessons:
            await update.callback_query.message.reply_text("В этой теме пока нет уроков")
            return
        
        buttons = []
        for lesson in lessons:
            lesson_id = str(abs(hash(lesson)))[:8]
            buttons.append([InlineKeyboardButton(lesson, callback_data=f"lesson_{lesson_id}")])
            context.user_data[f"lesson_{lesson_id}"] = lesson
        
        
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_topics")])
        
        await update.callback_query.message.reply_text(
            f"📚 Тема: <b>{user.topic}</b>\nВыберите урок:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        await update.callback_query.message.reply_text("⚠️ Ошибка при загрузке уроков")