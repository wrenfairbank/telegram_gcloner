#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


@restricted
def start(update, context):
    update.message.reply_text('先上传包含SA文件的ZIP压缩包，并在标题填写 /sa\n'
                              '再 /folders 设置收藏的文件夹。\n'
                              '随后转发或直接发送带有google drive链接的内容即可。')
