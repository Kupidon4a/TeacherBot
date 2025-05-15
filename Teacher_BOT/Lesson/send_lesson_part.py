from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
async def send_lesson_part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lesson_data = context.user_data['current_lesson']
    current_index = lesson_data['current_index']
    parts = lesson_data['parts']
    title = lesson_data['title']
    total = lesson_data['total_parts']
    
    #Прогресс-бар
    progress = min(int((current_index + 1) / total * 10), 10)
    progress_bar = f"[{'=' * progress}{' ' * (10 - progress)}] {current_index + 1}/{total}"
    
    message = f"📖 {title}\n{progress_bar}\n\n{parts[current_index]}"
    
    if current_index < total - 1:
        buttons = [[InlineKeyboardButton("Далее ▶️", callback_data="next_step")]]
    else:
        buttons = [[InlineKeyboardButton("✅ Начать тест", callback_data="start_test")]]
    
    if current_index == 0:
        await update.callback_query.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await update.callback_query.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons)
        )