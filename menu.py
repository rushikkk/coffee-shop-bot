#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3



def menu(bot, update):
    conn = sqlite3.connect('xmpl-coffee-shop-db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menu_coffee")
    rows = c.fetchall()
    print(rows[0][1])

    keyboard = [[InlineKeyboardButton(rows[0][1], callback_data='1'), InlineKeyboardButton(rows[2][1], callback_data='3')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    conn.close()


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)