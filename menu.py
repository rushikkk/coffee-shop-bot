#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,\
 CallbackQueryHandler, ConversationHandler
from datetime import datetime
import coffee_sqlite
from emoji import emojize

COFFEE, SIZE, SYRUP, BILL = range(4)
sql_query = ['' for i in range(6)]


def menu(bot, update):
    keyboard = [
        [InlineKeyboardButton("MENU", callback_data='choosing')],
        [InlineKeyboardButton("LAST ORDER", callback_data='last_order')],
        [InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="PRESS 'MENU'",
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            "PRESS 'MENU'",
            reply_markup=reply_markup
        )
    return COFFEE


def coffee(bot, update, user_data):
    query = update.callback_query
    sql_query[0] = update.effective_user['id']
    keyboard = []
    user_data['coffees'] = coffee_sqlite.select_items('menu_coffee')
    for data in user_data['coffees']:
        keyboard.append([InlineKeyboardButton('\U00002615 ' + str(data[1]),
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("\U00002B05 BACK", callback_data='back'),
                     InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Choose coffee:",
        reply_markup=reply_markup
    )
    return SIZE


def coffee_size(bot, update, user_data):
    query = update.callback_query
    for data in user_data['coffees']:
        if data[0] == int(query.data):
            user_data['coffee'] = data[1]
            user_data['is_syrup'] = data[3]
            user_data['is_size'] = data[4]
            sql_query[1] = data[0]
            break
    keyboard = []
    user_data['sizes'] = coffee_sqlite.select_sizes(sql_query[1])
    for data in user_data['sizes']:
        keyboard.append([InlineKeyboardButton(emojize(":scales: ", use_aliases=True) + str(data[2]) + 'mL, ' + str(data[3]) + ' BYN',
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("\U00002B05 BACK", callback_data='back'),
                     InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Choose size:",
        reply_markup=reply_markup
    )
    return SYRUP


def syrup(bot, update, user_data):
    query = update.callback_query
    for data in user_data['sizes']:
        if data[0] == int(query.data):
            user_data['size'] = data[2]
            sql_query[5] = data[0]
            user_data['cost'] = data[3]
            break
    keyboard = []
    user_data['syrups'] = coffee_sqlite.select_items('menu_syrup')
    for data in user_data['syrups']:
        keyboard.append([InlineKeyboardButton(emojize(data[3]) + str(data[1]) + ', ' + str(data[2]) + ' BYN',
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("\U00002B05 BACK", callback_data='back'),
                     InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="CHOOSE SYRUP",
        reply_markup=reply_markup
    )
    return BILL


def bill(bot, update, user_data):
    query = update.callback_query
    for data in user_data['syrups']:
        if data[0] == int(query.data):
            user_data['syrup'] = data[1]
            sql_query[2] = data[0]
            user_data['cost'] += data[2]
            sql_query[3] = user_data['cost']
            break
    sql_query[4] = datetime.now()
    coffee_sqlite.insert_order(sql_query)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Your order is:\n\tCoffee: {coffee}\n\t'
             'Syrup: {syrup}\n\tSize: {size}mL\n\t'
             'Price: {cost} BYN'.format(**user_data)
    )
    return ConversationHandler.END


def last_order(bot, update):
    query = update.callback_query
    user_id = [update.effective_user['id']]
    l_order = coffee_sqlite.last_order(user_id)
    if l_order:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Your last order is:\n\tCoffee: {}\n\t'
                 'Syrup: {}\n\tSize: {}mL\n\t'
                 'Price: {} BYN'.format(*l_order)
        )
    else:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='You have not ordered anything yet!'
        )
    return ConversationHandler.END


def reset(bot, update):
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Your order is canceled!'
    )
    return ConversationHandler.END


def unknown(bot, update):
    """Unknown command"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Unknown command. Type /help for help.')


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],

        states={
            COFFEE: [CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(last_order, pattern='^last_order$'),
                     CallbackQueryHandler(coffee, pass_user_data=True),
                     ],
            SIZE:   [CallbackQueryHandler(menu, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(coffee_size, pass_user_data=True),
                     ],
            SYRUP:  [CallbackQueryHandler(menu, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(syrup, pass_user_data=True),
                     ],
            BILL:   [CallbackQueryHandler(coffee, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(bill, pass_user_data=True),
                     ]
        },

        fallbacks=[CommandHandler('menu', menu)]
    )
