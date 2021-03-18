import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from dsbot.client import BotClient

logging.basicConfig(level=logging.WARNING)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--token", default=settings.SLACK_TOKEN, help="Slack token")

    def handle(self, verbosity, token, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(verbosity)
        )

        BotClient(token=token).start()
