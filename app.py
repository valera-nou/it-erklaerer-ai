import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  
    

@app.route("/erklaere", methods=["POST"])
def erklaere_begriff():
    data = request.get_json()

    if not data or "begriff" not in data:
        return jsonify({"fehler": "Bitte einen 'begriff' im JSON-Body übergeben."}), 400

    begriff = data["begriff"].strip()
    if not begriff:
        return jsonify({"fehler": "Der Begriff darf nicht leer sein."}), 400

    prompt = f"""Erkläre den IT-Begriff "{begriff}" auf Deutsch kurz und verständlich.
Gib außerdem ein praktisches Code-Beispiel (bevorzugt Python).

Antworte im folgenden JSON-Format:
{{
  "begriff": "{begriff}",
  "erklaerung": "Kurze Erklärung hier...",
  "code_beispiel": "# Code hier..."
}}

Antworte NUR mit dem JSON-Objekt, ohne weiteren Text oder Markdown-Blöcke."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher IT-Erklärer. Du antwortest immer auf Deutsch und ausschließlich mit gültigem JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
    except Exception as e:
        
        result = {
            "fehler": "OpenAI API Problem",
            "details": str(e)
        }


    result = json.loads(response.choices[0].message.content)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)