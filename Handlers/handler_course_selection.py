from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes
)

from Data_Base.database import db
from Menu.teacher import teacher
from User.user import user

#Выбор курса
async def handle_course_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_disciplines":
        await teacher(update, context)
        return
    
    try:
        if user.get_topic() != None or user.get_title() != None:
            print(f"Выбранный пользователем курс - {user.get_course()}")
            print(f"Выбранная пользователем тема - {user.get_topic()}")
            print(f"Выбранный пользователем урок - {user.get_title()}")
            
            await query.message.reply_text(f"❌ Ошибка сценария использования. Пожалуйста не нажимайте кнопки не в последнем сообщении от бота!")
            return
        course = query.data.replace("course_", "")
        course = context.user_data.get(query.data)
        
        user.set_course(course)
        print(f"Пользователем {user.get_login()} Выбран курс {user.get_course()}")
        user.set_course(user.get_course())
        
        if not user.get_discipline():
            await query.message.reply_text("❌ Ошибка: дисциплина не выбрана")
            return
        
        topics = db.get_topics(user.discipline, user.course)

        if not topics:
            available_courses = db.get_courses(user.discipline)
            await query.message.reply_text(
                f" В курсе '{user.get_course()}' из дисциплины {user.get_discipline()} нет тем.\n"
                f"Доступные курсы: {', '.join(available_courses)}"
            )
            return
        
        buttons = []
        for topic in topics:
            topic_id = str(abs(hash(topic)))[:8]
            buttons.append([InlineKeyboardButton(topic, callback_data=f"topic_{topic_id}")])
            context.user_data[f"topic_{topic_id}"] = topic
        
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_courses")])
        
        await query.message.reply_text(
            f"📚 Курс: <b>{user.course}</b>\nВыбери тему:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
    
    except Exception as e:
        print(f"Ошибка в handle_course_selection: {str(e)}")
        await query.message.reply_text("⚠️ Произошла ошибка при загрузке тем")