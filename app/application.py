import weave
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import json
from model import DimensionModel, FlashCardModel
from prompt import make_prompt, extract_facts_prompt


# API KEY AND MODEL
load_dotenv()
model = "mistral-small-latest"

application = Flask(__name__)

# Define a route for the root URL ("/")
@application.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@application.route('/process_text', methods=['POST'])
def process_text():
    weave.init('Prod monitoring')
    # Process the input text and display page with restul?
    if request.method == 'POST':
        data = request.form['text']
        dimension_model = DimensionModel(model_name=model)
        countStr = dimension_model(data)
        print(countStr)
        count = int(countStr['count']) if int(countStr['count']) < 5 else 5
        if count < 1:
            return jsonify({}), 200
        flash_card_model = FlashCardModel()
        cards = flash_card_model.predict(data, count)
        front_format = [{"front": c["question"], "back": c["answer"], "tags": c["tags"]} for c in cards]
        return jsonify(front_format), 200


if __name__ == '__main__':
    application.run(port=8000 ,debug=True)