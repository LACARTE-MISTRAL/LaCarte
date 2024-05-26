from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import os

# API KEY AND MODEL
load_dotenv()

model = "mistral-large-latest"
app = Flask(__name__)
app.secret_key = os.getenv("LA_CLE_MISTRAL")

# Define a route for the root URL ("/")
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process_text', methods=['POST'])
def process_text():
    # Process the input text and display page with restul?
    if request.method == 'POST':
        data = request.form['text']
        print(data)
    return "Results"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242 ,debug=True)
    