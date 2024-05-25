import json
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
import weave
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


class ExtractFlashCard(weave.Model):
    model_name: str
    prompt_template: str = (
        'Generate a list of flashcard questions and answers as a JSON array of objects in the format '
        '{"question": <str>, "answer": <str>, "tags": <str[]>} to test retention of the factual'
        ' information in the following text:')

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
    model = ExtractFlashCard(model_name="mistral-large-latest")

    sentence = ("Élève de Poufsouffle, participant au tournoi des trois sorciers. Né en 1977, fils de Amos Diggory,"
                " il est assassiné le 24 juin 1995 par Queudver (Peter Pettigrow) sous les ordres de Voldemort. En 1993, en cinquième"
                " année, il devint le capitaine de l’équipe de quidditch où il joue comme attrapeur. C'est un très bon élève et il "
                " devient également préfet. En 1994, Cedric est sélectionné par la Coupe de Feu pour représenter Poudlard au Tournoi"
                " des Trois Sorciers. Il devient très proche de Cho Chang, ce qui rend Harry jaloux.  À la dernière épreuve du"
                " tournoi, il remporte celui-ci, ex æquo avec Harry Potter, et touchant ensemble la coupe qui était en fait un "
                " Portoloin, ils sont tous deux envoyés auprès de Voldemort, dans le cimetière de son père. C’est là qu’il est"
                " assassiné par Peter Pettigrow sous les yeux de Harry.")

    print(asyncio.run(model.predict(sentence)))
