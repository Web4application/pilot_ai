import os
import openai
from flask import Flask, request, render_template, jsonify
from fadaka import mint_fdak
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if user_input.startswith("mint"):
        _, amount, _, to = user_input.split()
        tx = mint_fdak(to, amount)
        return jsonify({"response": f"✅ Minted {amount} FDAK to {to}\nTx: {tx}"})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({"response": response.choices[0].message["content"]})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    content = file.read().decode()
    prompt = f"Explain this file:\n\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"response": response.choices[0].message["content"]})

if __name__ == '__main__':
    app.run(debug=True)
