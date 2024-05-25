json_schema = """
    {
        front: string,
        back: string,
        tags: string[]
    }
"""
def make_prompt(n, text):
    return "Generate " + str(n) + " flashcard questions and answers as a JSON array of objects in the format `" + json_schema + "` to test retention of the factual information in the following text: \"" + text + "\""


def extract_facts_prompt(text):
    return "Analyze the following text and identify the number of distinct factual statements it contains. Provide the count of factual statements as a JSON array of objects in the format `{ count :  number of facts }`'. Text: \"" + text + "\""