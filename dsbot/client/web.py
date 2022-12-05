import logging

import slack_sdk.web

logger = logging.getLogger(__name__)


class WebClient(slack_sdk.web.WebClient):
    def custom_thread_parent(
        self,
        *,
        channel: str,
        thread_ts: str,
    ):
        logger.debug("Looking up parent for %s %s", channel, thread_ts)
        # https://api.slack.com/methods/conversations.history
        # Fetch the parent post
        post = self.conversations_history(
            channel=channel,
            latest=thread_ts,
            limit=1,
            inclusive=True,
        )
        parent = post["messages"][0]
        parent["channel"] = channel
        return parent
