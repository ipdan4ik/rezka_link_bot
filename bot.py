import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from get_link import send_mail, receive_mail, parse_link
from settings import config

TELEGRAM_KEY = config['TELEGRAM_KEY']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    send_mail()
    await asyncio.sleep(3)
    mail = receive_mail()
    hd_link = parse_link(mail)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{hd_link}'
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_KEY).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
