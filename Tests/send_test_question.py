from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    )


async def send_test_question(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lesson_data = context.user_data['current_lesson']
    current_index = lesson_data['current_question']
    questions = lesson_data['test_questions']
    question = questions[current_index]
    
    message = f"📝 Тест\nВопрос {current_index + 1}/{len(questions)}\n\n{question['text']}"
    context.user_data['waiting_for_text_answer'] = True
    
    if update.callback_query:
        reply_target = update.callback_query.message
    elif update.message:
        reply_target = update.message
    else:
        reply_target = None

    if not reply_target:
        return

    if question['type'] == 'multiple_choice':
        buttons = [
            [InlineKeyboardButton(f"{i+1}. {option}", callback_data=f"answer_{i}")]
            for i, option in enumerate(question['options'])
        ]
        await reply_target.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        if update.callback_query:
            await update.callback_query.message.reply_text(
                message + "\n\nНапишите ваш ответ в чат",
                reply_markup=None
            )
        elif update.message:
            await update.message.reply_text(
                message + "\n\nНапишите ваш ответ в чат",
                reply_markup=None
            )   