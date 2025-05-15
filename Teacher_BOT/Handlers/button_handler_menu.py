from telegram import Update
from telegram.ext import (
    ContextTypes
)
import asyncio
from Menu.teacher import teacher
from Menu.help import help
from Stop.stop import stop

async def button_handler_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'menu_button_teacher':
        await asyncio.sleep(1)
        await teacher(update, context)
    elif query.data == 'menu_button_help':
        await help(update, context)
    elif query.data == 'menu_button_stop':
        await stop(update, context)