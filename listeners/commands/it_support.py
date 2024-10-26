from slack_bolt import Ack, Respond
from logging import Logger

# Replace with your actual channel ID
IT_SUPPORT_CHANNEL_ID = "C0123456789"

def it_support_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        channel_id = command['channel_id']
        user_id = command['user_id']
        user_input = command.get('text', '')

        if channel_id != IT_SUPPORT_CHANNEL_ID:
            respond(
                response_type="ephemeral",
                text=f"Sorry <@{user_id}>, the `/it-support` command can only be used in <#{IT_SUPPORT_CHANNEL_ID}> channel."
            )
            logger.info(f"Unauthorized use of /it-support by <@{user_id}> in channel <#{channel_id}>.")
            return

        # Respond publicly, including the user's input
        bot_message = (f"<@{user_id}> requested IT support: {user_input}\n"
                       f"Currently, we can't help you. You can call 123-456-7890 for help")
        respond(
            response_type="in_channel",
            text=bot_message
        )
    except Exception as e:
        logger.error(f"Error in it_support_callback: {e}")