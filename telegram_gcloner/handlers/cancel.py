#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CallbackQueryHandler

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CallbackQueryHandler(cancel, pattern=r'^cancel$'))


def cancel(update, context):
    query = update.callback_query
    # query.message.edit_reply_markup(reply_markup=None)
    query.message.delete()
