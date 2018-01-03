#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters
import logging
import bot_token
from menu import conv_handler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
    %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Start the Bot"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Введите /menu для отображения меню."
                     "\nВведите /help для справки.")


def help_menu(bot, update):
    """Show help menu"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="<b>Доступные команды:</b>"
                     "\n\t/menu - отобразить меню"
                     "\n\t/help - отобразить раздел справки\n",
                     parse_mode='HTML')


def unknown(bot, update):
    """Unknown command"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Unknown command. Type /help for help.')


def main():

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=bot_token.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # start function
    dp.add_handler(CommandHandler('start', start))

    # /help command
    dp.add_handler(CommandHandler('help', help_menu))

    dp.add_handler(conv_handler)

    # Trigger for unknown command
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start the bot
    updater.start_polling()

    # updater.start_webhook()
    updater.idle()


if __name__ == '__main__':
    main()
