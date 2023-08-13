import asyncio
import json
import time

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from get_link import send_mail, receive_mail, parse_link
from settings import MAIN_CONFIG
from loguru import logger

TELEGRAM_KEY = MAIN_CONFIG['TELEGRAM_KEY']


def get_link_cached(chat_id):
    cache = json.load(open('link.json', 'r'))
    if time.time() - cache['time'] < 3600:
        logger.success(f'[{chat_id}] Using link from cache.')
        return cache['link']

    logger.info(f'[{chat_id}] Sending mail.')
    send_mail()
    logger.info(f'[{chat_id}] Receiving mail.')
    mail = receive_mail()
    if not mail:
        logger.warning(f'[{chat_id}] Mail not received. Using link from cache.')
        return cache['link']
    hd_link = parse_link(mail)
    logger.success(f'[{chat_id}] Got new link.')
    return hd_link


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info('Got request from user')
    chat_id = update.effective_chat.id
    link = get_link_cached(chat_id)
    await context.bot.send_message(
        chat_id=chat_id,
        text=f'{link}'
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_KEY).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
