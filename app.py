import json
import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        content = request.form["animal"]
        keywords = extract_keywords(content)
        return redirect(url_for("index", result=repr(keywords)))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route('/parse', methods=['POST'])
def parse():
    content = request.json.get('content')
    if content is None or type(content) != str:
        return json.dumps({
            'code': -1,
            'message': ''
        }), 400

    keywords = extract_keywords(content)
    return json.dumps(
        {
            'code': 0,
            'message': 'success',
            'keywords': keywords
        }
    ), 200


def extract_keywords(content):
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=generate_prompt(content),
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )
    print(response)
    result = response.choices[0].text
    result = result.split("\n")
    res = []
    for line in result:
        line = line.replace('-', '')
        if line == '':
            continue
        tokens = line.split(',')
        for token in tokens:
            res.append(token)
    return res


def generate_prompt(content):
    return "extract keywords from this text:\n\n" + content
