from slack_bolt import App
from .it_support import it_support_callback


def register(app: App):
    app.command("/it-support")(it_support_callback)
