from pydantic import BaseModel


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