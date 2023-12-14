import logging
from functools import wraps

from dsbot.conf import settings
from slack.errors import SlackApiError
from .exceptions import channel_errors
from dsbot import util

logger = logging.getLogger(__name__)


def ignore_users(ignore_user_list=settings.SLACK_IGNORE_USERS):
    def _outer(func):
        @wraps(func)
        def _inner(*args, data, **kwargs):
            if data.get("user") in ignore_user_list:
                logger.debug("Ignoring user %s", data["user"])
            else:
                return func(*args, data=data, **kwargs)

        return _inner

    return _outer


def ignore_bots(func):
    @wraps(func)
    def _inner(*args, data, **kwargs):
        if util.is_bot(data):
            logger.debug("Skipping bot message %s", data)
        else:
            return func(*args, data=data, **kwargs)

    return _inner


def ignore_subtype(func):
    @wraps(func)
    def __inner(*args, message, **kwargs):
        if subtype := message.get("subtype", None):
            logger.debug("%s skips subtype message %s", func, subtype)
        else:
            return func(*args, message=message, **kwargs)

    return __inner


def api_error(func):
    @wraps(func)
    def __inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SlackApiError as e:
            if e.response.data["error"] in channel_errors:
                raise channel_errors[e.response.data["error"]](
                    response=e.response, **kwargs
                ) from e
            raise e

    return __inner
