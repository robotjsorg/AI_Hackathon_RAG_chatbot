# AI_Hackathon_RAG_chatbot
Slack chatbot written in Python, powered by RAG (Retrieval-Augmented Generation.)

## Setup

Install the dependencies for server:
```
pip install -r server/requirements.txt
```


## Server

To run the server, run the following command:
```
OPEN_AI_KEY=<Put OpenAI Key Here> python server/app.py
```


## Slackbot

Once the RAG server is up and running, start the Slackbot.
```
SLACK_BOT_TOKEN=<Put Slack Bot Token Here> SLACK_APP_TOKEN=<Put Slack App Token Here> python app.py
```
