# AI_Hackathon_RAG_chatbot
Slack chatbot written in Python, powered by RAG (Retrieval-Augmented Generation.)

## Setup

Install the dependencies for server:
```
pip install -r server/requirements.txt
```
In your `server/.env` file, you should include:
```
OPEN_AI_KEY=<Put OpenAI Key Here>
ALLOW_RESET=TRUE
```


## RAG Server

To run the RAG server, run the following command:
```
python server/app.py
```


## Slackbot

Once the RAG server is up and running, start the Slackbot.
```
SLACK_BOT_TOKEN=<Put Slack Bot Token Here> SLACK_APP_TOKEN=<Put Slack App Token Here> python app.py
```
