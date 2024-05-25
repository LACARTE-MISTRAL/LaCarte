from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
import os

def mistral(user_message, model="mistral-small-latest", is_json=True):
    client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))
    messages = [ChatMessage(role="user", content=user_message)]

    if is_json:
        chat_response = client.chat(
            model=model, 
            messages=messages,
            response_format={"type": "json_object"})
    else:
        chat_response = client.chat(
            model=model, 
            messages=messages)
        
    return chat_response.choices[0].message.content

