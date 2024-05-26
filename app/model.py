import json

from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
import weave
import os


class FlashCardModel(weave.Model):
    model_name: str = "mistral-small-latest"
    json_schema: str = """
    {
        front: string,
        back: string,
        tags: string[]
    }"""

    prompt_template: str = (f"Generate {{count}} flashcard questions and answers as a JSON array of objects in the format "
                            f"`{json_schema}` to test retention of the factual information in the following text: ")

    @weave.op()
    def __call__(self, user_message, count, is_json=True):

        sysprompt = self.prompt_template.replace("{count}", str(count))

        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = client.chat(
            model=self.model_name,
            messages=[ChatMessage(role='system', content=sysprompt),
                      ChatMessage(role="user", content=user_message)],
            response_format={"type": "json_object"}
        )

        return chat_response.choices[0].message.content


class DimensionModel(weave.Model):
    model_name: str = "mistral-small-latest"
    prompt_template: str = ("Analyze the following text and identify the number of distinct factual statements it contains."
                            " Provide the count of factual statements as a JSON array of objects in the format "
                            "`{ count : int }`'. Text: ")

    @weave.op()
    def __call__(self, user_message, is_json=True):
        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = client.chat(
            model=self.model_name,
            messages=[ChatMessage(role='system', content=self.prompt_template),
                      ChatMessage(role="user", content=user_message)],
            response_format={"type": "json_object"}
        )

        try:
            count = json.loads(chat_response.choices[0].message.content)
        except json.JSONDecodeError:
            count = {'count': 2}
        return count


dimension_model = DimensionModel()
flash_card_model = FlashCardModel()

