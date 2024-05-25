import json
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
import weave
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


class ExtractFruitsModel(weave.Model):
    model_name: str
    prompt_template: str

    @weave.op()
    async def predict(self, sentence: str) -> dict:
        client = MistralAsyncClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = await client.chat(
            model=self.model_name,
            messages=[ChatMessage(role='system', content=self.prompt_template),
                      ChatMessage(role="user", content=sentence)],
            response_format={"type": "json_object"}
        )

        result = chat_response.choices[0].message.content

        if result is None:
            raise ValueError("No response from model")
        parsed = json.loads(result)
        return parsed


if __name__ == '__main__':
    weave.init('intro-example')
    model = ExtractFruitsModel(model_name="mistral-small-latest",
                               prompt_template='Extract fields ("fruit": <str>, "color": <str>, "flavor": <str>) from the following text, as json: {sentence}')

    sentence = "There are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy."
    print(asyncio.run(model.predict(sentence)))
