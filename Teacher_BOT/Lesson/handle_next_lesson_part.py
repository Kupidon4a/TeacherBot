from telegram import Update
from telegram.ext import ContextTypes

from Lesson.send_lesson_part import send_lesson_part

async def handle_next_lesson_part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lesson_data = context.user_data['current_lesson']
    lesson_data['current_index'] += 1
    await send_lesson_part(update, context)