from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import os
import json
from mistral import mistral
from prompt import make_prompt, extract_facts_prompt


# API KEY AND MODEL
load_dotenv()
model = "mistral-large-latest"

application = Flask(__name__)

# Define a route for the root URL ("/")
@application.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@application.route('/process_text', methods=['POST'])
def process_text():
    # Process the input text and display page with restul?
    if request.method == 'POST':
        data = request.form['text']
        countStr = mistral(extract_facts_prompt(data))
        try:
            countStr = json.loads(countStr)
        except:
            countStr = {'count': 2}
        print(countStr)
        count = int(countStr['count']) if int(countStr['count']) < 8 else 8
        if count < 1:
            return jsonify({}), 200
        response = mistral(make_prompt(count , data))
        cards = json.loads(response)
    return jsonify(cards), 200


if __name__ == '__main__':
    application.run(port=8000 ,debug=True)