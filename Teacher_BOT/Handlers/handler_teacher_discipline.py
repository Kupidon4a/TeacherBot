from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes
)

from Data_Base.database import db
from validation import *
from Menu.menu import menu
from User.user import user

async def handle_teacher_discipline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "teacher_back":
        await menu(update, context)
        return
    
    if user.get_course() != None or user.get_topic() != None or user.get_title() != None:
        print(user.get_discipline())
        print(user.get_course())
        print(user.get_topic())
        print(user.get_title())
        
        await query.message.reply_text(f"❌ Ошибка сценария использования. Пожалуйста не нажимайте никакие кнопки не в последнем сообщении от бота!")
        return

    discipline = query.data.replace("teacher_disc_", "")
    user.set_discipline(discipline)
    print(f"Пользователем {user.get_login()} Выбрана дисциплина - {user.get_discipline()}")

    courses = db.get_courses(user.discipline)
    if not courses:
        await query.message.reply_text(f"❌ В дисциплине '{user.get_discipline()}' нет доступных курсов.")
        return
    
    buttons = []
    for course in courses:
        course_id = str(abs(hash(course)))[:8]
        buttons.append([InlineKeyboardButton(course, callback_data=f"course_{course_id}")])
        [InlineKeyboardButton(course, callback_data=f"course_{course}")]
        context.user_data[f"course_{course_id}"] = course

    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_disciplines")])
    
    await query.message.reply_text(
        f"📖 Дисциплина: <b>{discipline}</b>\nВыбери курс:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )