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
syrups = c.fetchall()
conn.close()

order = {}


def menu(bot, update):
    order.clear()
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
    # print(coffee.__name__)
    # print(update)
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
    for data in coffees:
        if data[0] == int(query.data):
            order['coffee'] = data[1]
            order['cost'] = data[2]
            break
    keyboard = []
    for data in syrups:
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
    query = update.callback_query
    for data in syrups:
        if data[0] == int(query.data):
            order['syrup'] = data[1]
            order['cost'] += data[2]
            break
    # print(order)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Ваш заказ:\nКофе: {coffee}\nСироп: {syrup}\nСтоимость заказа: {cost}'.format(**order)
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],

        states={
            COFFEE: [CallbackQueryHandler(coffee)],
            SYRUP:  [CallbackQueryHandler(syrup)],
            BILL:   [CallbackQueryHandler(bill)]
        },

        fallbacks=[CommandHandler('menu', menu)]
    )
