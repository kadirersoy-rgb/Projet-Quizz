import os
import hashlib
import hmac

from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from jwt_utils import build_token, decode_token, JwtError
from questions import add_question
from question_model import Question

# Charger les variables du fichier .env
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/questions', methods=['POST'])
def PostQuestion():
    # Récupérer le token depuis Authorization
    authorization = request.headers.get('Authorization')

    if not authorization or not authorization.startswith('Bearer '):
        return "Unauthorized", 401

    token = authorization.split(' ', 1)[1]

    try:
        decode_token(token)
    except JwtError:
        return "Unauthorized", 401

    # Récupérer les informations de la question
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return {"error": "Invalid JSON"}, 400

    title = payload.get('title')
    text = payload.get('text')
    image = payload.get('image')
    position = payload.get('position')

    if not isinstance(title, str) or not isinstance(text, str):
        return {"error": "Invalid question"}, 400

    try:
        question = Question(title=title, text=text, image=image, position=position)
        question_id = add_question(question)
    except ValueError:
        return {"error": "Invalid position"}, 400

    return {"id": question_id}, 200


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return "Unauthorized", 401

    password = payload.get("password")

    if not isinstance(password, str):
        return "Unauthorized", 401

    # Calculer le hash MD5 du mot de passe reçu
    hashed = hashlib.md5(password.encode("UTF-8")).digest()

    # Récupérer le hash attendu depuis .env
    expected_hash = os.getenv("ADMIN_PASSWORD_MD5")

    if not expected_hash:
        return {"error": "Admin password not configured"}, 500

    try:
        expected_hash_bytes = bytes.fromhex(expected_hash)
    except ValueError:
        return {"error": "Invalid admin password configuration"}, 500

    # Comparer les deux hash
    if hmac.compare_digest(hashed, expected_hash_bytes):
        token = build_token()
        return {"token": token}, 200

    return "Unauthorized", 401


@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"


if __name__ == "__main__":
    app.run()
