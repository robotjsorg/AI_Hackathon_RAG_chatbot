from slack_bolt import Ack, Respond
from logging import Logger


def it_support_summary(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = command["user_id"]

        # Define your table data
        table_data = [
            [
                "Total questions resolved",
                "Total likes",
                "Total dislikes",
                "Average response time",
                "Satisfaction rate",
                "Resolved percentage",
                "Date",
            ],
            [123, 98, 5, 15.2, 94.3, 98.7, "2024-10-16"],
            [87, 75, 3, 12.4, 95.8, 97.1, "2024-10-15"],
            [150, 130, 10, 14.8, 92.0, 99.3, "2024-10-14"],
            [200, 180, 8, 13.7, 95.5, 98.0, "2024-10-13"],
            [175, 160, 7, 16.1, 93.1, 97.5, "2024-10-12"],
            [220, 210, 12, 11.5, 94.9, 98.8, "2024-10-11"],
            [140, 120, 6, 10.9, 96.0, 97.8, "2024-10-10"],
            [95, 85, 2, 13.3, 97.7, 99.0, "2024-10-09"],
            [180, 170, 9, 12.8, 95.0, 98.4, "2024-10-08"],
            [160, 150, 5, 14.2, 96.3, 98.6, "2024-10-07"],
        ]

        respond(
            response_type="in_channel",
            blocks=[
                # User's request
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<@{user_id}> requested IT Support Summary*\n>",
                    },
                },
                # Divider
                {"type": "divider"},
                # Bot's response
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":robot_face: *Slackbot Response:*\nIT Support Summay\n{table_data}\n",
                    },
                },
                # Context block indicating it's generated by the Slackbot
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": "This feature is coming soon!"}
                    ],
                },
            ],
        )
    except Exception as e:
        logger.error(f"Error in it_support_callback: {e}")
