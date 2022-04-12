import logging
import re

MENTION_REGEX = re.compile("^<@(|[WU].+?)>(.*)")
LINK_REGEX = re.compile(r"<(http.*?)(\|.*?)?>", re.DOTALL)

logger = logging.getLogger(__name__)


def parse_direct_mention(message_text):
    """
    Finds a direct mention (a mention that is at the beginning) in message text
    and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = MENTION_REGEX.search(message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


# Parse URLs
# https://api.slack.com/docs/message-formatting#linking_to_urls
def parse_links(message_text):
    for m in LINK_REGEX.findall(message_text):
        logger.debug("Found match %s", m)
        yield m[0]


def extract_text(message):
    print(message)
    if 'blocks' in message:
        def _element(element):
            for e in element['elements']:
                if 'text' in e:
                    yield e['text']
                else:
                    yield str(e)
            
        def _blocks(blocks):
            for block in blocks:
                if "text" in block:
                    yield block["text"]["text"]
                elif block['type'] == 'rich_text':
                    for element in block['elements']:
                        yield ' '.join(_element(block['elements']))

        return '\n'.join(_blocks(message['blocks']))

    else:
        return message['text']
