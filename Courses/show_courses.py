from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    )

from Data_Base.database import db
from User.user import user

async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        courses = db.get_courses(user.discipline)
        buttons = []
        for course in courses:
            course_id = str(abs(hash(course)))[:8]
            buttons.append([InlineKeyboardButton(course, callback_data=f"course_{course_id}")])
            context.user_data[f"course_{course_id}"] = course
        
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_disciplines")])
        
        await update.callback_query.message.reply_text(
            f"📖 Дисциплина: <b>{user.discipline}</b>\nВыбери курс:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка в show_courses: {str(e)}")
        await update.callback_query.message.reply_text("⚠️ Ошибка при загрузке курсов")