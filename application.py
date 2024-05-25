from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import os
import json
from mistral import mistral
from prompt import make_prompt

# API KEY AND MODEL
load_dotenv()
model = "mistral-large-latest"

application = Flask(__name__)

# Define a route for the root URL ("/")
@application.route('/')
def home():
    return render_template('index.html')


@application.route('/process_text', methods=['POST'])
def process_text():
    # Process the input text and display page with restul?
    if request.method == 'POST':
        data = request.form['text']
        response = mistral(make_prompt(1, data))
        card = json.loads(response)
    return render_template('index.html', question=card["front"], answer=card["back"])

if __name__ == '__main__':
    application.run(port=8000 ,debug=True)