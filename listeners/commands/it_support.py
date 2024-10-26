from slack_bolt import Ack, Respond
from logging import Logger


def it_support_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        respond(f"Hello World")
    except Exception as e:
        logger.error(e)
