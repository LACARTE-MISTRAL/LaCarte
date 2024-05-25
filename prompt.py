def make_prompt(n, text):
    return "Generate " + str(n) + " flashcard questions and answers in the JSON format `{ question: string, answer: string }` to test retention of the factual information in the following text: \"" + text + "\""
