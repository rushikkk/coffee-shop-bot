#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters
from telegram import ReplyKeyboardRemove
import logging
import bot_token
from menu import conv_handler
from telegram.ext.dispatcher import run_async

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
    %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


@run_async
def start(bot, update):
    """Start the Bot"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Введите /menu для отображения меню."
                          "\nВведите /help для справки.")


@run_async
def help_menu(bot, update):
    """Show help menu"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="<b>Доступные команды:</b>"
                          "\n\t/menu - отобразить меню"
                          "\n\t/help - отобразить раздел справки\n",
                     parse_mode='HTML')


@run_async
def unknown(bot, update):
    """Unknown command"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Unknown command. Type /help for help.',
                     reply_markup=ReplyKeyboardRemove())


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

    # Start the bot via WebHook
    # updater.start_webhook(listen='127.0.0.1', port=5000, url_path='<TOKEN>')
    # updater.bot.set_webhook(url='https://<DOMAIN_NAME>/<TOKEN>')
    # NGINX config:
    # server  {
    #   server_name <DOMAIN_NAME>;
    #   listen  443 ssl;
    #   ssl_certificate /path/to/fullchain.pem; #Let's Encrypt certificate
    #   ssl_certificate_key /path/to/privkey.pem;
    #   ssl_trusted_certificate /path/to/chain.pem;
    #   location /<TOKEN> {
    #       proxy_pass  http://127.0.0.1:5000;
    #   }
    # }

    # updater.start_webhook()
    updater.idle()


if __name__ == '__main__':
    main()
