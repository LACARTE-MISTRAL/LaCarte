import asyncio
import os

import weave

from evaluation.data_model import SquadDataset
from kudo_model import ExtractFlashCard
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


if __name__ == '__main__':
    model = ExtractFlashCard(model_name="mistral-small-latest")

    with open('../datasets/train-v2.0.json') as f:
        data = json.load(f)

    sd = SquadDataset.parse_obj({"data": data["data"][:10]})

    contexts_examples = [sd.data[i].paragraphs[j].context for i in range(len(sd.data))
                         for j in range(len(sd.data[i].paragraphs))]

    golden_qas = [sd.data[i].paragraphs[j].qas for i in range(len(sd.data)) for j in range(len(sd.data[i].paragraphs))]

    examples = [
        {'id': '0', 'sentence': contexts_examples[0], 'target': {"qas": golden_qas[0], "sentence": contexts_examples[0]}},
        {'id': '1', 'sentence': contexts_examples[1], 'target': {"qas": golden_qas[1], "sentence": contexts_examples[1]}},
        {'id': '2', 'sentence': contexts_examples[2], 'target': {"qas": golden_qas[2], "sentence": contexts_examples[2]}}
    ]

    weave.init('qa_gen_evaluator')

    @weave.op()
    def mistral_as_a_judge(target: dict, model_output: dict) -> dict:

        # Compute a representativity_metric
        words_in_context = set(target['sentence'].split(' '))
        words_in_model_output = set([q for qa in model_output for q in qa['question'].split(' ')] + [q for qa in model_output for q in qa['answer'].split(' ')])
        words_in_golden = set([q for qa in target['qas'] for q in qa['question'].split(' ')] + [q for qa in target['qas'] for q in qa['answers'][0]['text'].split(' ')] )

        representativity_metric = (len(words_in_model_output.intersection(words_in_context)) /
                                    max(1, len(words_in_golden.intersection(words_in_context))))

        # Compute a correctness_metric
        ## LLM AS A JUDGE

        client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))

        chat_response = client.chat(
            model="mistral-large-latest",
            messages=[ChatMessage(role='system', content="Is this answer correct? Answer ONLY with the number of good responces. Nothing else."),
                      ChatMessage(role="user", content=f"QUESTIONS/ANSWER PAIRS : {[(qa['question'],  qa['answer']) for qa in model_output]}" + f"\n CONTEXT : {target['sentence']} \n RESPONSE (a number between 0 and {len(model_output)}: ")]
        )

        correctness_metric = int(chat_response.choices[0].message.content) / len(model_output)

        return {'representativity_metric': representativity_metric, "correctness_metric": correctness_metric}

    evaluation = weave.Evaluation(
        dataset=examples,
        scorers=[mistral_as_a_judge])

    print(asyncio.run(evaluation.evaluate(model)))
