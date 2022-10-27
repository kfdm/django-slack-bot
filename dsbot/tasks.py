from celery import shared_task
from slack_sdk.web.client import WebClient

from dsbot import exceptions
from dsbot.conf import settings

default_client = WebClient(token=settings.SLACK_TOKEN)


# Wrapped version of Slack API Calll
# We want to make it easy to rate limit our calls to slack by wrapping
# it as a shared_task.
@shared_task(rate_limit=settings.SLACK_RATE_LIMIT)
def api_call(*args, **kwargs):
    try:
        return default_client.api_call(*args, json=kwargs).data
    except exceptions.SlackApiError as e:
        exceptions.cast_slack_exception(e, **kwargs)


@shared_task(rate_limit=TASK_RATE_LIMIT)
def celery_api_call(*args, **kwargs):
    try:
        result = default_client.api_call(*args, **kwargs)
    except exceptions.SlackApiError as e:
        exceptions.cast_slack_exception(e, **kwargs)
    else:
        return result.data


class CeleryClient(WebClient):
    task_kwargs = False

    def api_call(self, *args, **kwargs):
        if self.task_kwargs is False:
            return celery_api_call.delay(*args, **kwargs).forget()
        else:
            return celery_api_call.delay(*args, **kwargs).get(**self.task_kwargs)

    def __enter__(self) -> "CeleryClient":
        self.task_kwargs = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.task_kwargs = False


client = CeleryClient(token=settings.SLACK_TOKEN)
