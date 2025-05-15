from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from Data_Base.database import db
from Courses.show_courses import show_courses

from User.user import user

async def handle_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_courses":
        try:
            await show_courses(update, context)
        except Exception as e:
            print(f"Ошибка при возврате к курсам: {str(e)}")
            await query.message.reply_text("⚠️ Ошибка при загрузке курсов")
        return
    
    if user.get_course() == None or user.get_topic() != None or user.get_title() != None:
        print(user.get_course())
        print(user.get_topic())
        print(user.get_title())
        
        await query.message.reply_text(f"❌ Ошибка сценария использования. Пожалуйста не нажимайте кнопки не в последнем сообщении от бота!")
        return

    try:
        topic_id = query.data.replace("topic_", "")
        topic_name = context.user_data.get(f"topic_{topic_id}")
        
        if not topic_name:
            await query.message.reply_text("❌ Тема не найдена")
            return
        
        user.set_topic(topic_name)
        print(f"Пользователем с логином {user.get_login()} выбрана тема {user.get_topic()}")
        lessons = db.get_lessons(user.discipline, user.course, user.topic)
        
        if not lessons:
            await query.message.reply_text(f"❌ В теме '{user.get_topic()}' из курса {user.get_course()} из дисциплины {user.get_discipline()} нет уроков")
            return
        
        buttons = []
        for lesson in lessons:
            lesson_id = str(abs(hash(lesson)))[:8]
            buttons.append([InlineKeyboardButton(lesson, callback_data=f"lesson_{lesson_id}")])
            context.user_data[f"lesson_{lesson_id}"] = lesson
        
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_topics")])
        
        await query.message.reply_text(
            f"📝 Тема: <b>{topic_name}</b>\nВыбери урок:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
    
    except Exception as e:
        print(f"Ошибка в handle_topic_selection: {str(e)}")
        await query.message.reply_text("⚠️ Ошибка при загрузке уроков")