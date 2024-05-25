import json
from pydantic import BaseModel

with open('train-v2.0.json') as f:
    data = json.load(f)


class SquadQA(BaseModel):
    question: str
    id: str
    answers: list[dict]
    is_impossible: bool


class SquadQAS(BaseModel):
    context: str
    qas: list[SquadQA]


class SquadSample(BaseModel):
    title: str
    paragraphs: list[SquadQAS]


class SquadDataset(BaseModel):
    data: list[SquadSample]


sd = SquadDataset.parse_obj({"data": data["data"][:10]})
