#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,\
 CallbackQueryHandler, ConversationHandler
import sqlite3

COFFEE, SYRUP, BILL = range(3)

conn = sqlite3.connect('xmpl-coffee-shop-db.db')
c = conn.cursor()
c.execute("SELECT * FROM menu_coffee")
coffees = c.fetchall()
c.execute("SELECT * FROM menu_syrup")
cyrups = c.fetchall()
conn.close()


def menu(bot, update):
    keyboard = [
        [InlineKeyboardButton("MENU", callback_data=str(COFFEE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "PRESS 'MENU'",
        reply_markup=reply_markup
    )
    return COFFEE


def coffee(bot, update):
    query = update.callback_query
    keyboard = []
    for data in coffees:
        keyboard.append([InlineKeyboardButton(str(data[1]),
                        callback_data=data[0])])
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="CHOOSE COFFEE",
        reply_markup=reply_markup
    )
    return SYRUP


def syrup(bot, update):
    query = update.callback_query
    keyboard = []
    for data in cyrups:
        keyboard.append([InlineKeyboardButton(str(data[1]),
                        callback_data=data[0])])
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="CHOOSE SYRUP",
        reply_markup=reply_markup
    )
    return BILL


def bill(bot, update):
    pass


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],

        states={
            COFFEE: [CallbackQueryHandler(coffee)],
            SYRUP:  [CallbackQueryHandler(syrup)],
            BILL:   [CallbackQueryHandler(bill)]
        },

        fallbacks=[CommandHandler('menu', menu)]
    )
