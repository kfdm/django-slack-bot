"""
Base Bot Class

The base bot class is mostly concerned with maintaining
the connection to Slack, and then dispatching events to
the Dispatcher

A few convenencie functions used by commands are also
added to the bot class
"""


import inspect
import logging
import re

import slack_sdk.rtm

from dsbot.client.web import WebClient
from dsbot.exceptions import CommandError

logger = logging.getLogger(__name__)


class BotClient(slack_sdk.rtm.RTMClient):
    user_id = None
    _commands = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._web_client = WebClient(
            token=self.token,
            base_url=self.base_url,
            timeout=self.timeout,
            ssl=self.ssl,
            proxy=self.proxy,
            run_async=self.run_async,
            loop=self._event_loop,
            session=self._session,
            headers=self.headers,
        )

    @classmethod
    def cmd(cls, key):
        """A decorator to store and link a callback to an event."""

        def decorator(callback):
            logger.debug("Registering %s %s", key, callback)
            cls._validate_callback(callback)
            cls._commands.append(
                {
                    "key": key,
                    "re": re.compile(key),
                    "func": callback,
                    "help": callback.__doc__.strip().split("\n")[0],
                }
            )
            return callback

        return decorator

    async def _dispatch_command(self, command, data=None):
        for cmd in self._commands:
            match = cmd["re"].match(command)
            if match:
                try:
                    if inspect.iscoroutinefunction(cmd["func"]):
                        logger.debug("Running %(key)s %(func)s as async", cmd)
                        return await cmd["func"](
                            rtm_client=self,
                            web_client=self._web_client,
                            data=data,
                            match=match,
                        )
                    else:
                        logger.debug("Running %(key)s %(func)s as thread", cmd)
                        return cmd["func"](
                            rtm_client=self,
                            web_client=self._web_client,
                            data=data,
                            match=match,
                        )
                except CommandError as e:
                    logger.warning("Command Error")
                    return self._web_client.chat_postEphemeral(
                        as_user=True,
                        channel=data["channel"],
                        user=data["user"],
                        attachments=[
                            {
                                "color": "warning",
                                "title": "Command Error",
                                "text": str(e),
                            }
                        ],
                    )
                except Exception as e:
                    logger.exception("Unknown Error")
                    return self._web_client.chat_postEphemeral(
                        as_user=True,
                        channel=data["channel"],
                        user=data["user"],
                        attachments=[
                            {
                                "color": "danger",
                                "title": "Unknown Error",
                                "text": str(e),
                            }
                        ],
                    )
