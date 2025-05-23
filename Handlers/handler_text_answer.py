from telegram import Update
from telegram.ext import (
    ContextTypes
)

from Data_Base.database import db
from validation import *

from User.user import user
from Tests.finish_test import finish_test
from Tests.send_test_question import send_test_question

async def handle_text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('waiting_for_text_answer'):
        await update.message.reply_text("⚠️ Сейчас не ожидается текстовый ответ. Пожалуйста, следуйте инструкциям.")
        return
    
    lesson_data = context.user_data['current_lesson']
    current_question = lesson_data['current_question']
    questions = lesson_data['test_questions']
    question = questions[current_question]
    
    # Обработка ответа
    if question['type'] == 'multiple_choice':
        query = update.callback_query
        await query.answer()
        selected_answer = int(query.data.replace("answer_", ""))
        correct_answer = int(question['correct_answer'])
        
        user_answer_text = question['options'][selected_answer]
        correct_answer_text = question['options'][correct_answer]

        if selected_answer == correct_answer:
            is_correct_answer = True
            lesson_data['correct_answers'] += 1
            feedback = "✅ Верно!"
        else:
            is_correct_answer = False
            feedback = f"❌ Неверно! Правильный ответ: {question['options'][correct_answer]}"
        
        await query.message.reply_text(feedback)
    
    else:
        user_answer = update.message.text
        correct_answer = question['correct_answer']
        user_answer_text = user_answer
        correct_answer_text = correct_answer

        if user_answer.lower() == correct_answer.lower():
            is_correct_answer = True
            lesson_data['correct_answers'] += 1
            feedback = "✅ Верно!"
        else:
            is_correct_answer = False
            feedback = f"❌ Неверно! Правильный ответ: {correct_answer}"
        
        await update.message.reply_text(feedback)
    db.add_result_test(user.get_login(), user.get_discipline(), user.get_course(), user.get_topic(), lesson_data['title'], question["text"], user_answer_text, correct_answer_text, is_correct_answer)
    # Переходим к следующему вопросу или завершаем тест
    if current_question < len(questions) - 1:
        lesson_data['current_question'] += 1
        await send_test_question(update, context)
    else:
        await finish_test(update, context)
    return