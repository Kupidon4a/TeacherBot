from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    )

async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message if update.message else update.callback_query.message
    lesson_data = context.user_data['current_lesson']
    total_questions = len(lesson_data['test_questions'])
    correct_answers = lesson_data['correct_answers']
    score = int(correct_answers / total_questions * 100)
    
    result_message = (
        f"📊 Результаты теста:\n"
        f"Правильных ответов: {correct_answers}/{total_questions}\n"
        f"Оценка: {score}%\n\n"
    )
    if score >= 80:
        result_message += "Отличный результат! 🎉"
    elif score >= 60:
        result_message += "Хороший результат! 👍"
    else:
        result_message += "Попробуйте изучить урок ещё раз. 🔄"
    context.user_data['waiting_for_text_answer'] = False
    
    await message.reply_text(
        result_message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 К списку уроков", callback_data="back_to_lessons")]
        ])
    )
    return