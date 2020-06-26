#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import logging

from telegram import ParseMode
from telegram.ext import Dispatcher, CommandHandler
from telegram.utils.helpers import mention_html

from utils.config_loader import config
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('4999baoyue', contact, pass_args=True))


@restricted
def contact(update, context):
    if update.message.text.strip('/4999baoyue'):
        context.bot.send_message(chat_id=config.USER_IDS[0],
                                 text='Received message from {} ({}):'.format(
                                     mention_html(update.effective_user.id, html.escape(update.effective_user.name)),
                                     update.effective_user.id),
                                 parse_mode=ParseMode.HTML)
        context.bot.forward_message(chat_id=config.USER_IDS[0],
                                    from_chat_id=update.message.chat_id,
                                    message_id=update.message.message_id)
        update.message.reply_text('收到。')
    else:
        update.message.reply_text('这么害羞，不说点啥？\n' +
                                  config.AD_STRING.format(context.bot.username),
                                  ParseMode.HTML)
