import asyncio
import os

import weave

from app.evaluation.data_model import SquadDataset
from app.model import FlashCardModel
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import dotenv


mistral_model="mistral-small-latest"

dotenv.load_dotenv()


if __name__ == '__main__':
    model = FlashCardModel(model_name="mistral-small-latest")

    with open('train-v2.0.json') as f:
        data = json.load(f)

    sd = SquadDataset.parse_obj({"data": data["data"][:10]})

    contexts_examples = [sd.data[i].paragraphs[j].context for i in range(len(sd.data))
                         for j in range(len(sd.data[i].paragraphs))]

    golden_qas = [sd.data[i].paragraphs[j].qas for i in range(len(sd.data)) for j in range(len(sd.data[i].paragraphs))]

    examples = [
        {'id': str(i), 'user_message': contexts_examples[i], 'count': 8,
         'target': {"qas": golden_qas[i], "sentence": contexts_examples[i]}}
        for i in range(1,500,50)
    ]

    weave.init('qa_gen_evaluator')

    @weave.op()
    def mistral_as_a_judge(target: dict, model_output: dict) -> dict:

        # Compute a representativity_metric

        # words_in_context = set(target['sentence'].split(' '))
        # words_in_model_output = set([q for qa in model_output for q in qa['question'].split(' ')] + [q for qa in model_output for q in qa['answer'].split(' ')])
        # words_in_golden = set([q for qa in target['qas'] for q in qa['question'].split(' ')] + [q for qa in target['qas'] for q in qa['answers'][0]['text'].split(' ')] )
        #
        # representativity_metric = (len(words_in_model_output.intersection(words_in_context)) /
        #                             max(1, len(words_in_golden.intersection(words_in_context))))

        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        try:
            chat_response = client.chat(
                model=mistral_model,
                messages=[ChatMessage(role='system',
                                      content="Give a number between 0% and 100% to indicate which part of the input context text is covered by"
                                              "the generated questions/answers. Answer ONLY with a number. Nothing else."),
                          ChatMessage(role="user",
                                      content=f"QUESTIONS/ANSWER PAIRS : {model_output}" + f"\n CONTEXT : {target['sentence']} \n RESPONSE (a number between 0 and 100 nothing else): ")]
            )

            representativity_metric = int(chat_response.choices[0].message.content.replace('%', '')) / 100

        except Exception:

            representativity_metric = 0

        # Compute a correctness_metric
        ## LLM AS A JUDGE
        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = client.chat(
            model=mistral_model,
            messages=[ChatMessage(role='system', content="Is this answer correct? Answer ONLY with the number of good responces. Nothing else."),
                      ChatMessage(role="user", content=f"QUESTIONS/ANSWER PAIRS : {model_output}" + f"\n CONTEXT : {target['sentence']} \n RESPONSE (a number between 0 and {len(model_output)} nothing else): ")]
        )

        try:
            correctness_metric = int(chat_response.choices[0].message.content.split('\n')[0]) / len(model_output)
        except:
            correctness_metric = 0

        # Compute a redundoncy_metric
        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = client.chat(
            model=mistral_model,
            messages=[ChatMessage(role='system',
                                  content="How many questions/answers are redundant? Answer ONLY with a number. Nothing else."),
                      ChatMessage(role="user",
                                  content=f"QUESTIONS/ANSWER PAIRS : {model_output}" + f"\n CONTEXT : {target['sentence']} \n RESPONSE (a number between 0 and {len(model_output)} nothing else): ")]
        )

        try:
            redundoncy_metric = int(chat_response.choices[0].message.content.split('\n')[0]) / len(model_output)
        except:
            redundoncy_metric = 0

        return {'representativity_metric': representativity_metric,
                "correctness_metric": correctness_metric,
                "redundoncy_metric": redundoncy_metric}

    evaluation = weave.Evaluation(
        dataset=examples,
        scorers=[mistral_as_a_judge])

    print(asyncio.run(evaluation.evaluate(model)))
