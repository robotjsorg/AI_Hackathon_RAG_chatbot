from slack_bolt import App
from .it_support import it_support_callback
from .it_summary import it_summary


def register(app: App):
    app.command("/it-support")(it_support_callback)
    app.command("/it-summary")(it_summary)
