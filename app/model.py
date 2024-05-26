import json
from groq import Groq
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
import weave
import os


class FlashCardModel(weave.Model):
    model_name: str = "mistral-medium-latest"
    json_schema: str = """
    {
        question: string,
        answer: string,
        tags: string[]
    }"""

    prompt_template: str = (f"Generate {{count}} flashcard questions and answers as a JSON array of objects in the format "
                            f"`{json_schema}` to test retention of the factual information in the following text: ")

    @weave.op()
    def predict(self, user_message: str, count: int, is_json=True):

        sysprompt = self.prompt_template.replace("{count}", str(count))

        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))
        

        chat_response = client.chat(
            model=self.model_name,
            messages=[ChatMessage(role='system', content=sysprompt),
                      ChatMessage(role="user", content=user_message)],
            response_format={"type": "json_object"}
        )
        return json.loads(chat_response.choices[0].message.content)

    def __name__(self):
        return "FlashCardModel"


class DimensionModel(weave.Model):
    model_name: str = "mixtral-8x7b-32768"
    prompt_template: str = ("Analyze the following text and identify the number of distinct factual statements it contains."
                            " Provide the count of factual statements as a JSON array of objects in the format "
                            "`{ count : int }`'. Text: ")

    @weave.op()
    def __call__(self, user_message, is_json=True):

        client = Groq(api_key=os.getenv("GROK_API_KEY"))

        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt_template

                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            temperature=1,
            max_tokens=5000,
            top_p=1,
            stream=False,
            stop=None,
            response_format={"type" : "json_object"}
        )

        try:
            response = json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError:
            response = {'count': 2}

        return response
        



dimension_model = DimensionModel()
flash_card_model = FlashCardModel()

