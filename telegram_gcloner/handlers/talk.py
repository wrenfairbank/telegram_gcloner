#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import html
import logging
import re

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from utils.config_loader import config
from utils.helper import alert_users
from utils.restricted import restricted_admin, restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('talk', set_talk, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(set_talk, pattern=r'^talk(,\d+)?'))


@restricted_admin
def set_talk(update, context):
    query = update.callback_query
    chat_id = None
    if query:
        match = re.search(r'^talk(?:,(?P<chat_id>\d+))?$', query.data)
        if match:
            if match.group('chat_id'):
                chat_id = int(match.group('chat_id'))
        else:
            alert_users(context, update.effective_user, 'invalid query', query.data)
            query.answer(text='哟呵', show_alert=True)
            return
    else:
        if context.args:
            try:
                chat_id = int(context.args[0])
            except Exception as e:
                update.message.reply_text('非法对话对象，请重试。{}'.format(e))
                return

    if not chat_id:
        context.user_data['talk'] = None
        update.message.reply_text('已取消对话对象。')
        return

    try:
        chat = context.bot.get_chat(chat_id)
        context.user_data['talk'] = chat_id
        message = '成功将对话对象设置为：{} ({})'.format(
            mention_html(chat_id, html.escape(' '.join(filter(None, [chat.first_name, chat.last_name])))), chat_id)
        if chat.username:
            message += f' (@{chat.username})'
        context.bot.send_message(chat_id=update.effective_user.id, text=message, parse_mode=ParseMode.HTML)
    except Exception as e:
        error_message = '无法对话对象，请重试。{}'.format(e)
        if query:
            query.answer(error_message)
        else:
            update.message.reply_text(error_message)
        return


@restricted
def talk_to_admin(update, context):
    # talk to admin
    datetime_now = datetime.datetime.now()
    if datetime_now - context.user_data.get('last_time_we_talked', datetime_now - datetime.timedelta(minutes=10)) \
            > datetime.timedelta(minutes=5):
        context.user_data['last_time_we_talked'] = datetime_now
        inline_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton('对话', callback_data='talk,{}'.format(update.effective_user.id))]])
        message = 'Received message from {} ({})'.format(
                                     mention_html(update.effective_user.id,
                                                  html.escape(update.effective_user.full_name)),
                                     update.effective_user.id)
        if update.effective_user.username:
            message += f' (@{update.effective_user.username})'
        context.bot.send_message(chat_id=config.USER_IDS[0],
                                 text=message,
                                 reply_markup=inline_keyboard,
                                 parse_mode=ParseMode.HTML)


@restricted_admin
def talk_to_user(update, context):
    if context.user_data.get('talk', None):
        try:
            chat_id = context.user_data['talk']
            if update.message.text:
                context.bot.send_message(chat_id=chat_id, text=update.message.text)
            elif update.message.photo:
                context.bot.send_photo(chat_id=chat_id,
                                       photo=update.message.photo[-1]['file_id'],
                                       caption=update.message.caption,
                                       disable_web_page_preview=True)
            elif update.message.sticker:
                context.bot.send_sticker(chat_id=chat_id, sticker=update.message.sticker['file_id'])
            elif update.message.animation:
                context.bot.send_animation(chat_id=chat_id, animation=update.message.animation['file_id'])
            else:
                return
            update.message.reply_text('Message relayed to {}'.format(mention_html(chat_id, str(chat_id))),
                                      parse_mode='HTML')
        except Exception as e:
            update.message.reply_text('Unsuccessful: {}'.format(e))
        return
