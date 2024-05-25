from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_session import Session

application = Flask(__name__)

# Define a route for the root URL ("/")
@application.route('/')
def home():
    return render_template('index.html')


@application.rotue('/process_text', methods=['POST'])
def process_text():
    # Process the input text and display page with restul?
    return "Results"

if __name__ == '__main__':
    application.run(port=8000 ,debug=True)