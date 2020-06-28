#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.callback import callback_delete_message
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('help', get_help))


@restricted
def get_help(update, context):
    message = '发送google drive链接，或者转发带有google drive的信息即可手动转存。\n' \
              '需要使用 /sa 和 /folders 进行配置\n\n' \
              '以下是本BOT的命令：\n\n' \
              '/folders - 设置收藏文件夹\n' \
              '/sa - 仅限私聊，上传包含sa的ZIP文件夹，在标题写上/sa设置Service Account\n' \
              '/4999baoyue - 仅限私聊，商业洽谈，请附上留言\n' \
              '/help - 输出本帮助\n'
    rsp = update.message.reply_text(message)
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
