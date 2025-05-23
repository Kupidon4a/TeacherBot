from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    )

from Tests.send_test_question import send_test_question

async def start_lesson_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lesson_data = context.user_data['current_lesson']
    test_questions = lesson_data['test_questions']
    
    if not test_questions or len(test_questions) == 0:
        await query.message.reply_text(
            "Тест для этого урока не найден.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 К списку уроков", callback_data="back_to_lessons")]
            ])
        )
        return
    
    # Начинаем тест с первого вопроса
    lesson_data['current_question'] = 0
    lesson_data['correct_answers'] = 0
    await send_test_question(update, context)
    return