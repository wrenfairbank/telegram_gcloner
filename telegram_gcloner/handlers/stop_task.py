#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import re

from telegram.ext import Dispatcher, CallbackQueryHandler

from utils.helper import alert_users
from utils.restricted import restricted

logger = logging.getLogger(__name__)

regex_stop_task = r'^stop_task,(\d+)'


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CallbackQueryHandler(stop_task, pattern=regex_stop_task))


@restricted
def stop_task(update, context):
    query = update.callback_query
    if query.data:
        match = re.search(regex_stop_task, query.data)
        if match:
            thread_id = int(match.group(1))
            tasks = context.user_data.get('tasks', None)
            if tasks:
                for t in tasks:
                    if t.native_id == thread_id:
                        t.kill()
                        return
    alert_users(context, update.effective_user, 'invalid query data', query.data)
    query.answer(text='哟呵', show_alert=True)
    return
