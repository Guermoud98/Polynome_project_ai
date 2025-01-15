from flask import Flask, jsonify, request
import joblib
import numpy as np
from quiz_generator import generate_question_and_solution
import sympy as sp
import re
import requests
import threading
import time
import logging


# Charger le modèle
model = joblib.load("quiz_question_model.pkl")

app = Flask(__name__)
# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "quiz-service"
SERVICE_PORT = 5012  # Port de votre service
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"
HOSTNAME = "127.0.0.1"  # Adresse IP ou hostname
def register_with_eureka():
    """
    Enregistre le service auprès d'Eureka et envoie des heartbeats périodiques.
    """
    while True:
        try:
            url = EUREKA_SERVER + SERVICE_NAME
            payload = {
                "instance": {
                    "instanceId": INSTANCE_ID,
                    "hostName": HOSTNAME,
                    "app": SERVICE_NAME.upper(),
                    "ipAddr": HOSTNAME,
                    "vipAddress": SERVICE_NAME,
                    "status": "UP",
                    "port": {"$": SERVICE_PORT, "@enabled": True},
                    "dataCenterInfo": {
                        "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
                        "name": "MyOwn"
                    }
                }
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 204:
                logging.info(f"Service {SERVICE_NAME} registered successfully with Eureka!")
            else:
                logging.error(f"Failed to register with Eureka: {response.status_code}, {response.text}")
        except Exception as e:
            logging.error(f"Error registering with Eureka: {e}")

        # Envoyer un heartbeat toutes les 30 secondes
        time.sleep(30)


def sanitize_polynomial(polynomial):
    """
    Nettoie un polynôme pour le rendre compatible avec sympy.
    """
    sanitized = polynomial.replace("^", "**")
    sanitized = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', sanitized)
    sanitized = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', sanitized)
    sanitized = sanitized.replace(" ", "")
    return sanitized

def parse_polynomial(polynomial):
    """
    Analyse un polynôme et extrait les coefficients et caractéristiques.
    """
    x = sp.symbols('x')
    sanitized_polynomial = sanitize_polynomial(polynomial)

    try:
        expr = sp.sympify(sanitized_polynomial)
        coefficients = sp.Poly(expr, x).all_coeffs()

        # Normaliser les coefficients à une longueur de 10
        while len(coefficients) < 10:
            coefficients.insert(0, 0)
        coefficients = coefficients[-10:]

        degree = len(coefficients) - coefficients.count(0) - 1
        num_nonzero = np.count_nonzero(coefficients)
        max_coefficient = np.max(np.abs(coefficients))
        features = coefficients + [degree, num_nonzero, max_coefficient]

        return features

    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse du polynôme : {e}")

@app.route("/quiz", methods=["POST"])
def generate_quiz():
    """
    Génère un quiz basé sur un modèle entraîné.
    """
    data = request.get_json()
    polynomial = data.get("polynomial")

    try:
        features = parse_polynomial(polynomial)
        features = np.array(features).reshape(1, -1)

        question_type = model.predict(features)[0]
        question_and_solution = generate_question_and_solution(polynomial, question_type)

        return jsonify({
            "polynomial": polynomial,
            "question_type": question_type,
            "question": question_and_solution["question"],
            "solution": question_and_solution["solution"],
            "explanation": question_and_solution["explanation"]
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 400

if __name__ == "__main__":
    # Initialisation des logs
    logging.basicConfig(level=logging.INFO)

    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    logging.info(f"Démarrage du service {SERVICE_NAME} sur le port {SERVICE_PORT}.")
    app.run(host="0.0.0.0", port=SERVICE_PORT)
