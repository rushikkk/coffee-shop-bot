#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,\
 CallbackQueryHandler, ConversationHandler
from datetime import datetime
import coffee_sqlite

COFFEE, SYRUP, BILL = range(3)
order = {}
sql_query = ['' for i in range(5)]


def menu(bot, update):
    order.clear()
    keyboard = [
        [InlineKeyboardButton("МЕНЮ", callback_data='choosing')],
        [InlineKeyboardButton("ПОСЛЕДНИЙ ЗАКАЗ", callback_data='last_order')],
        [InlineKeyboardButton("ОТМЕНА", callback_data='reset')]
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


def coffee(bot, update):
    # print(coffee.__name__)
    query = update.callback_query
    sql_query[0] = update._effective_user.id
    keyboard = []
    global coffees
    coffees = coffee_sqlite.select_items('menu_coffee')
    for data in coffees:
        keyboard.append([InlineKeyboardButton(str(data[1]),
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("НАЗАД", callback_data='back'),
                     InlineKeyboardButton("ОТМЕНА", callback_data='reset')])
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
            sql_query[1] = data[0]
            order['cost'] = data[2]
            break
    keyboard = []
    global syrups
    syrups = coffee_sqlite.select_items('menu_syrup')
    for data in syrups:
        keyboard.append([InlineKeyboardButton(str(data[1]),
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("НАЗАД", callback_data='back'),
                     InlineKeyboardButton("ОТМЕНА", callback_data='reset')])
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
            sql_query[2] = data[0]
            order['cost'] += data[2]
            sql_query[3] = order['cost']
            break
    sql_query[4] = datetime.now()
    coffee_sqlite.insert_order(sql_query)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Ваш заказ:\n\tКофе: {coffee}\n\t'
             'Сироп: {syrup}\n\tСтоимость заказа: {cost}'.format(**order)
    )
    return ConversationHandler.END


def last_order(bot, update):
    query = update.callback_query
    user_id = [update._effective_user.id]
    l_order = coffee_sqlite.last_order(user_id)
    if l_order:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Ваш последний заказ:\n\tКофе: {}\n\t'
                 'Сироп: {}\n\tСтоимость заказа: {}'.format(*l_order)
        )
        # return BILL
    else:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Вы ещё ничего не заказывали!'
        )
    return ConversationHandler.END


def reset(bot, update):
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Вы отменили заказ!'
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
                     CallbackQueryHandler(coffee),
                     # CommandHandler('menu', menu),
                     # MessageHandler(Filters.command, unknown)
                     ],
            SYRUP:  [CallbackQueryHandler(menu, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(syrup),
                     # CommandHandler('menu', menu),
                     # MessageHandler(Filters.command, unknown)
                     ],
            BILL:   [CallbackQueryHandler(coffee, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(bill),
                     # CommandHandler('menu', menu),
                     # MessageHandler(Filters.command, unknown)
                     ]
        },

        fallbacks=[CommandHandler('menu', menu)]
    )
