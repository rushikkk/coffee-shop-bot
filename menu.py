#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,\
 CallbackQueryHandler, ConversationHandler
from datetime import datetime
import coffee_sqlite
from emoji import emojize

CHOSEN, COFFEE, SIZE, SYRUP, BILL, RETRY = range(6)
sql_query = ['' for i in range(6)]


def menu(bot, update):
    keyboard = [
        [InlineKeyboardButton("\U0001F4D6 MENU", callback_data='coffee')],
        [InlineKeyboardButton("\U0001F4C3 LAST ORDER", callback_data='last_order')],
        [InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Make a choice:",
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            "PRESS 'MENU'",
            reply_markup=reply_markup
        )
    return CHOSEN


def coffee(bot, update, user_data):
    query = update.callback_query
    sql_query[0] = update.effective_user['id']
    keyboard = []
    user_data['coffees'] = coffee_sqlite.select_items('bot_coffee')
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
    return COFFEE


def coffee_size(bot, update, user_data):
    query = update.callback_query
    if query.data != 'back_to_coffee_size':
        for data in user_data['coffees']:
            if data[0] == int(query.data):
                user_data['coffee'] = data[1]
                user_data['is_syrup'] = data[3]
                user_data['is_size'] = data[2]
                sql_query[1] = data[0]
                break
    if user_data['is_syrup'] == 0:
        back = 'back_to_coffee'
    else:
        back = 'back'
    keyboard = []
    user_data['sizes'] = coffee_sqlite.select_sizes(sql_query[1])
    for data in user_data['sizes']:
        keyboard.append([InlineKeyboardButton("\U00002696" + str(data[1]) + 'mL, ' + str(data[2]) + ' BYN',
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("\U00002B05 BACK", callback_data=back),
                     InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Choose size:",
        reply_markup=reply_markup
    )
    if user_data['is_syrup'] == 0:
        return SYRUP
    return SIZE


def syrup(bot, update, user_data):
    query = update.callback_query
    if query.data != 'back_to_syrup':
        for data in user_data['sizes']:
            if data[0] == int(query.data):
                user_data['size'] = data[1]
                sql_query[5] = data[0]
                user_data['cost'] = data[2]
                break
    keyboard = []
    user_data['syrups'] = coffee_sqlite.select_items('bot_syrup')
    if user_data['is_syrup'] == 0:
        back = 'back_to_coffee'
    else:
        back = 'back_to_coffee_size'
    for data in user_data['syrups']:
        keyboard.append([InlineKeyboardButton(emojize(data[2], use_aliases=True) + str(data[1]) + ', ' + str(data[3]) + ' BYN',
                        callback_data=data[0])])
    keyboard.append([InlineKeyboardButton("\U00002B05 BACK", callback_data=back),
                     InlineKeyboardButton("\U0000274E CANCEL", callback_data='reset')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Choose syrup:",
        reply_markup=reply_markup
    )
    return SYRUP


def bill(bot, update, user_data):
    query = update.callback_query
    if user_data['is_syrup'] == 0:
        for data in user_data['sizes']:
            if data[0] == int(query.data):
                user_data['size'] = data[1]
                sql_query[5] = data[0]
                user_data['cost'] = data[2]
                break
        user_data['syrup'] = 'Without syrup'
        sql_query[2] = 1
        sql_query[3] = user_data['cost']
    else:
        for data in user_data['syrups']:
            if data[0] == int(query.data):
                user_data['syrup'] = data[1]
                sql_query[2] = data[0]
                user_data['cost'] += data[3]
                sql_query[3] = user_data['cost']
                break
    sql_query[4] = datetime.now()
    # coffee_sqlite.insert_order(sql_query)
    user_data['sql_query'] = sql_query
    if user_data['is_syrup'] == 0:
        back = 'back_to_coffee_size'
    else:
        back = 'back_to_syrup'
    keyboard = [[InlineKeyboardButton("\U00002B05 BACK", callback_data=back),
                 InlineKeyboardButton("\U0001F197 YES", callback_data='retry')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_data['string'] = 'Coffee: {coffee}\n\tSyrup: {syrup}\n\tSize: {size}mL\n\tCurrent price: {cost} BYN\n\t'.format(**user_data)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Your order is:\n\t' + user_data['string'],
        reply_markup=reply_markup
    )
    return BILL


def last_order(bot, update, user_data):
    query = update.callback_query
    user_id = [update.effective_user['id']]
    l_order = coffee_sqlite.last_order(user_id)
    retry_order = [i for i in l_order[3:]]
    retry_order.insert(4, datetime.now())
    user_data['sql_query'] = retry_order
    user_data['string'] = 'Coffee: {0}\n\tSyrup: {1}\n\tSize: {2}mL\n\tCurrent price: {6}\n\t'.format(*l_order)
    if l_order:
        keyboard = [[InlineKeyboardButton("\U00002B05 BACK", callback_data='back_to_menu'),
                     InlineKeyboardButton("\U0001F197 YES", callback_data='retry')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Your last order is:\n\t' + user_data['string'] + 'Retry?',
            reply_markup=reply_markup
        )
        return BILL
    else:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='You have not ordered anything yet!'
        )
        return ConversationHandler.END


def last_order_retry(bot, update, user_data):
    query = update.callback_query
    coffee_sqlite.insert_order(user_data['sql_query'])
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=emojize('Your order is:\n\t' + user_data['string'])
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
            CHOSEN: [CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(last_order, pattern='^last_order$', pass_user_data=True),
                     CallbackQueryHandler(coffee, pass_user_data=True),
                     ],
            COFFEE: [CallbackQueryHandler(menu, pattern='^back$'),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(coffee_size, pass_user_data=True),
                     ],
            SIZE:   [CallbackQueryHandler(coffee, pattern='^back$', pass_user_data=True),
                     CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(syrup, pass_user_data=True),
                    ],
            SYRUP:  [CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(coffee, pattern='^back_to_coffee$', pass_user_data=True),
                     CallbackQueryHandler(coffee_size, pattern='^back_to_coffee_size$', pass_user_data=True),
                     CallbackQueryHandler(bill, pass_user_data=True),
                     ],
            BILL:   [CallbackQueryHandler(reset, pattern='^reset$'),
                     CallbackQueryHandler(coffee_size, pattern='^back_to_coffee_size$', pass_user_data=True),
                     CallbackQueryHandler(syrup, pattern='^back_to_syrup$', pass_user_data=True),
                     CallbackQueryHandler(menu, pattern='^back_to_menu$'),
                     CallbackQueryHandler(last_order_retry, pass_user_data=True),
                     ],
        },

        fallbacks=[CommandHandler('menu', menu)]
    )
