from slack_bolt import Ack, Respond
from logging import Logger
import random
import requests

# Replace with your actual channel ID
IT_SUPPORT_CHANNEL_ID = "C07TFNLM4LW"
IT_SUPPORT_SPECIALISTS = {
    "U07TKAX2M8D": "Max Tran"
}
LLM_CONTEXT_TEMPLATE = "" # TODO feed llm context from RAG here

VALIDATION_PROMPT_TEMPLATE = (
    "Given the general IT knowledge and this context {context}\n"
    "\n"
    "Here is the question: {prompt}. "
    "If the question is not related to IT, please reply with 'No, it is not an IT question'. "
    "Otherwise, reply with 'Yes, it is an IT question' and do not answer the question. "
)

SYSTEM_PROMPT = (
    "You are an IT support specialist with 20 years of experience working at one of the private tech company. Some of "
    "the IT knowledge questions you will be asked is public knowledge or only available to internal of your company"
)

# PROMPT_TEMPLATE = (
#     "You are an IT support. Given the general IT knowledge and this context {context}\n"
#     "\n"
#     "I'll ask you a question. If it's not an IT question, please reply with 'I can only answer IT questions'."
#     "else if it's an IT question and you know the answer, please give me a concise paragraph answer."
#     "else if it's an IT question but you don't know the answer because its related to internal information and tooling, "
#     "just reply with 'IDK, I will contact IT Specialist'\n"
#     "{prompt}"
# )

QUERY_PROMPT_TEMPLATE = (
    "Given my question {prompt}\n"
    "You can look for the answer in publicly available IT knowledge and this additional internal knowledge {context}\n"
    "Please give me a concise paragraph answer to my question if you can find the answer. "
    "Otherwise, if you can't find or can't help or don't know, only reply with 'IDK, I will contact IT Specialist' "
    "and please do not say anything else.\n"
)

def get_it_specialist_id():
    it_specialist_list = list(IT_SUPPORT_SPECIALISTS.keys())
    it_specialist_id = random.choice(it_specialist_list)
    print(f'The chosen it specialist: {it_specialist_id}')
    return it_specialist_id

def generate_llm_response(prompt):
    import ollama
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

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

# Out of scope
def build_prompt(messages):
    prompt = ''
    for message in messages:
        if message['role'] == 'system':
            prompt += f"{message['content']}\n\n"
        elif message['role'] == 'user':
            prompt += f"User: {message['content']}\n\n"
        elif message['role'] == 'assistant':
            prompt += f"Assistant: {message['content']}\n\n"
    return prompt


def call_rag(query):
    print("Calling RAG")
    url = 'http://10.104.150.13:5001/retrieve'
    headers = {'Content-Type': 'application/json'}
    data = {"query": query}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check if the request was successful

        # Print the response (assuming it's JSON)
        print("Response JSON:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("An error occurred:", err)

def converse_with_ollama(initial_question, model='llama3.2'):
    root_messages = []
    root_messages.append({'role': 'system', 'content': SYSTEM_PROMPT})
    llm_context = call_rag(initial_question)
    # llm_context = LLM_CONTEXT_TEMPLATE
    print(f"llm_context: {llm_context}")

    # Build validation prompt
    validation_prompt = VALIDATION_PROMPT_TEMPLATE.format(
        context=llm_context,
        prompt=initial_question
    )
    validation_messages = root_messages + [{'role': 'user', 'content': validation_prompt}]

    # Build prompt string for validation
    prompt = build_prompt(validation_messages)

    # Validate IT question via first prompt
    validation_response = generate_llm_response(prompt)
    print(f"Validation response: {validation_response}")

    validation_messages.append({'role': 'assistant', 'content': validation_response})

    if "yes" in validation_response.lower():
        # User repeats the initial question for the assistant to answer
        user_prompt = QUERY_PROMPT_TEMPLATE.format(
            context=llm_context,
            prompt=initial_question
        )
        query_messages = root_messages + [{'role': 'user', 'content': user_prompt}]
        print(f"query_messages: {query_messages}")
        # Build prompt string for query
        query_prompt = build_prompt(query_messages)
        print(f"query_prompt: {query_prompt}")
        # Get the assistant's answer
        query_response = generate_llm_response(query_prompt)
        print(f"query_response: {query_response}")
        if 'idk' in query_response.lower() or 'sorry' in query_response.lower() or "can't" in query_response.lower():
            print("Choosing a specialist")
            it_specialist_id = get_it_specialist_id()
            query_response += f"\n<@{it_specialist_id}>, can you answer this?"
    else:
        query_response = validation_response

    assistant_reply = query_response
    print(f"Assistant: {assistant_reply}\n")
    return assistant_reply

def it_support_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        channel_id = command['channel_id']
        user_id = command['user_id']
        user_input = command.get('text', '')
        print(f'user_id: {user_id}')
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

        ollama_output = converse_with_ollama(user_input)

        respond(
            response_type="in_channel",
            blocks=[
                # User's request
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<@{user_id}> requested IT support:*\n>{user_input}"
                    }
                },
                # Divider
                {
                    "type": "divider"
                },
                # Bot's response
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":robot_face: *Slackbot Response:*\n{ollama_output}\n"
                    }
                },
                # Context block indicating it's generated by the Slackbot
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "_Generated by IT Support slackbot_"
                        }
                    ]
                }
            ]
        )
    except Exception as e:
        logger.error(f"Error in it_support_callback: {e}")