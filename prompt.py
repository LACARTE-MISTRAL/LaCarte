json_schema = """
    {
        front: string,
        back: string,
        tags: string[]
    }
"""
def make_prompt(n, text):
    return "Generate " + str(n) + " flashcard questions and answers in the JSON format `" + json_schema + "` to test retention of the factual information in the following text: \"" + text + "\""
