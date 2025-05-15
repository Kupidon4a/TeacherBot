from telegram import Update
from telegram.ext import ContextTypes

from Data_Base.database import db
from User.user import user

from User.user import *
from Lesson.send_lesson_part import send_lesson_part
from Lesson.handle_next_lesson_part import handle_next_lesson_part
from Tests.start_lesson_test import start_lesson_test
from Topics.show_topics import show_topics

async def handle_lesson_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_topics":
        await show_topics(update, context, await user.course)
        return
    
    try:
        # Обработка следующей части урока
        if query.data == "next_step":
            return await handle_next_lesson_part(update, context)
        
        # Обработка начала теста
        if query.data == "start_test":
            return await start_lesson_test(update, context)
        
        title = query.data.replace("lesson_", "")
        title = context.user_data.get(query.data)
        user.set_title(title)
        print(f"Пользователь с логином {user.get_login()} выбрал урок {user.get_title()}")
        lesson = db.get_lesson(
            user.get_discipline(),
            user.get_course(),
            user.get_topic(),
            user.get_title()
        )
        
        if not lesson:
            await query.message.reply_text("❌ Урок не найден")
            return
        
        # Получаем тест для этого урока
        test_questions = db.get_lesson_test(
            user.get_discipline(),
            user.get_course(),
            user.get_topic(),
            user.get_title()
        )
        # Сохраняем данные в контексте
        lesson_parts = lesson.split('\n\n')
        context.user_data['current_lesson'] = {
            'parts': lesson_parts,
            'current_index': 0,
            'title': title,
            'total_parts': len(lesson_parts),
            'test_questions': test_questions,
            'current_question': 0,
            'correct_answers': 0
        }
        
        # Отправляем первую часть
        await send_lesson_part(update, context)
        
    except Exception as e:
        print(f"Ошибка загрузки урока: {str(e)}")
        await query.message.reply_text("⚠️ Ошибка при загрузке урока")