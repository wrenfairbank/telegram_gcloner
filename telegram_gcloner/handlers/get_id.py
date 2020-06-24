#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('id', get_id))


@restricted
def get_id(update, context):
    if len(config.USER_IDS) and (update.message.chat.id not in config.USER_IDS):
        return
    update.message.reply_text(update.message.chat.id)
    logger.info('telegram user {0} has requested its id.'.format(update.message.chat.id))
