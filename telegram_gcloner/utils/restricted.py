#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from functools import wraps

from utils.config_loader import config

logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if not update.effective_user:
            return
        user_id = update.effective_user.id
        ban_list = context.bot_data.get('ban', [])
        # access control. comment out one or the other as you wish.
        # if user_id in ban_list:
        if user_id in ban_list or user_id not in config.USER_IDS:
            logger.info("Unauthorized access denied for {} {}.".format(update.effective_user.full_name, user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def restricted_user_ids(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if not update.effective_user:
            return
        user_id = update.effective_user.id
        if user_id not in config.USER_IDS:
            logger.info("Unauthorized access denied for {} {}.".format(update.effective_user.full_name, user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def restricted_admin(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if not update.effective_user:
            return
        user_id = update.effective_user.id
        if user_id != config.USER_IDS[0]:
            logger.info("Unauthorized admin access denied for {} {}.".format(update.effective_user.full_name, user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
