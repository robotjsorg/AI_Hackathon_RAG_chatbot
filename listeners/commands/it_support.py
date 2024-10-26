from slack_bolt import Ack, Respond
from logging import Logger
import ollama

# Replace with your actual channel ID
IT_SUPPORT_CHANNEL_ID = "C07TFNLM4LW"

def generate_llm_response(prompt):
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

# Out of scope
# def converse_with_ollama(initial_question, model='llama3.2'):
#     messages = [{'role': 'user', 'content': initial_question}]
#     while True:
#         # Send the messages to Ollama
#         response = ollama.chat(model=model, messages=messages)
#         assistant_reply = response['content']
#         print(f"Assistant: {assistant_reply}\n")
#
#         # Append the assistant's reply to the conversation
#         messages.append({'role': 'assistant', 'content': assistant_reply})
#
#         # Get the next user input
#         user_input = input("You: ")
#         if user_input.lower() in ('exit', 'quit'):
#             break
#         messages.append({'role': 'user', 'content': user_input})

def it_support_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        channel_id = command['channel_id']
        user_id = command['user_id']
        user_input = command.get('text', '')

        if channel_id != IT_SUPPORT_CHANNEL_ID:
            respond(
                response_type="ephemeral",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"<@{user_id}> requested IT support: {user_input}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Currently, we can't help you. You can call *123-456-7890* for help."
                        }
                    }
                ]
            )
            logger.info(f"Unauthorized use of /it-support by <@{user_id}> in channel <#{channel_id}>.")
            return

        ollama_output = generate_llm_response(user_input)
        print(ollama_output)
        bot_message = (f"<@{user_id}> requested IT support: {user_input}\n"
                       f"{ollama_output}")
        respond(
            response_type="in_channel",
            text=bot_message
        )
    except Exception as e:
        logger.error(f"Error in it_support_callback: {e}")