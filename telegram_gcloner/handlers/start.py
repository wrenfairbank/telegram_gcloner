#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.callback import callback_delete_message
from utils.config_loader import config
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


@restricted
def start(update, context):
    rsp = update.message.reply_text('先私聊上传包含SA文件的ZIP压缩包，并在标题填写 /sa\n'
                                    '再 /folders 设置收藏的文件夹。\n'
                                    '随后转发或直接发送带有google drive链接的内容即可。')
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
