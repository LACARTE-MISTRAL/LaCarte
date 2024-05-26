from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
from groq import Groq
import os

#def mistral(user_message, model="mistral-small-latest", is_json=True):
#    client = MistralClient(api_key=os.getenv("LA_CLE_MISTRAL"))
#    messages = [ChatMessage(role="user", content=user_message)]
#
#    if is_json:
#        chat_response = client.chat(
#            model=model, 
#            messages=messages,
#            response_format={"type": "json_object"})
#    else:
#        chat_response = client.chat(
#            model=model, 
#            messages=messages)
#        
#    return chat_response.choices[0].message.content
#

def call_groq(user_message, model="mixtral-8x7b-32768"):
    client = Groq()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "What to do in Paris"
            },
            {
                "role": "assistant",
                "content": "Paris, the capital city of France, is one of the most popular tourist destinations in the world, and for good reason. It is a city rich in history, culture, art, and cuisine, and there is no shortage of things to see and do. Here are some suggestions for what to do in Paris:\n\n1. Visit the Eiffel Tower: The iconic Eiffel Tower is a must-see attraction in Paris. You can take an elevator ride to the top for stunning views of the city.\n2. Explore the Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n3. Stroll through the Tuileries Garden: The Tuileries Garden is a beautiful public park located between the Louvre Museum and the Place de la Concorde. It's a great place to relax and take a break from sightseeing.\n4. Visit Notre-Dame Cathedral: Notre-Dame Cathedral is a stunning Gothic cathedral located on the Ile de la Cite. It's famous for its intricate architecture and beautiful stained glass windows.\n5. Shop on the Champs-Elysees: The Champs-Elysees is one of the most famous streets in the world, and it's a great place to shop for high-end fashion and luxury goods.\n6. Visit the Palace of Versailles: The Palace of Versailles is a stunning palace located just outside of Paris. It was once the royal residence of French kings and queens, and it's famous for its opulent decor and beautiful gardens.\n7. Take a boat ride on the Seine: The Seine River runs through the heart of Paris, and taking a boat ride is a great way to see some of the city's most famous landmarks, such as the Notre-Dame Cathedral and the Louvre Museum.\n8. Try French cuisine: Paris is known for its culinary scene, and there are countless restaurants and cafes throughout the city serving up delicious French cuisine.\n\nThese are just a few of the many things to see and do in Paris. Whether you're interested in history, art, culture, or cuisine, there's something for everyone in this beautiful city."
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
