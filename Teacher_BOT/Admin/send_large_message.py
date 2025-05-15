from telegram import Update
from Data_Base.database import db


#Отправка длинных сообщений в формате нескольких сообщений
async def send_large_message(update: Update, message):
    parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
    for part in parts:
        await update.effective_message.reply_text(part)
