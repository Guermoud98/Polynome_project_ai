from flask import Flask, request, jsonify
import joblib
import numpy as np
import sympy as sp
import requests
import threading
import time
import logging

# Charger le modèle et l'encodeur
model = joblib.load("method_classifier.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Initialiser l'application Flask
app = Flask(__name__)
# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "recommendation-service"
SERVICE_PORT = 5006  # Port de votre service
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"
HOSTNAME = "127.0.0.1"  # Adresse IP ou hostname

def register_with_eureka():
    """
    Fonction pour s'enregistrer auprès d'Eureka et envoyer des heartbeats périodiques.
    """
    while True:
        try:
            # URL pour enregistrer le service dans Eureka
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
                logging.info("Service registered successfully with Eureka!")
            else:
                logging.error(f"Failed to register with Eureka: {response.status_code}, {response.text}")
        except Exception as e:
            logging.error(f"Error registering with Eureka: {e}")

        # Envoyer un heartbeat toutes les 30 secondes
        time.sleep(30)

def parse_polynomial(polynomial):
    """
    Convertit un polynôme sous forme textuelle en une liste de coefficients et ajoute des caractéristiques supplémentaires.
    """
    x = sp.symbols('x')
    expr = sp.sympify(polynomial.replace("^", "**"))
    coefficients = sp.Poly(expr, x).all_coeffs()

    # Normaliser la liste des coefficients à une longueur de 10
    while len(coefficients) < 10:
        coefficients.insert(0, 0)

    coefficients = coefficients[-10:]  # Tronquer à 10 éléments

    # Ajouter des nouvelles caractéristiques
    num_nonzero = np.count_nonzero(coefficients)
    max_coefficient = np.max(coefficients)
    coefficients.append(num_nonzero)
    coefficients.append(max_coefficient)
    return coefficients

@app.route("/recommend", methods=["POST"])
def recommend_method_api():
    """
    Endpoint pour recommander une méthode basée sur le modèle pré-entraîné.
    """
    data = request.get_json()
    polynomial = data.get("polynomial")

    try:
        # Analyse du polynôme
        coefficients = parse_polynomial(polynomial)
        coefficients = np.array(coefficients).reshape(1, -1)

        # Vérifiez le degré du polynôme
        x = sp.symbols('x')
        expr = sp.sympify(polynomial.replace("^", "**"))
        degree = sp.Poly(expr, x).degree()

        if degree == 2:
            return jsonify({
                "recommended_method": "Quadratique",
                "explanation": f"Le polynôme est de degré 2, donc la méthode Quadratique est directement recommandée."
            })
        elif degree > 2:
            return jsonify({
                "recommended_method": "Newton",
                "explanation": f"Le polynôme est de degré {degree}, donc la méthode Newton est directement recommandée."
            })

        # Sinon, utilisez le modèle pour prédire
        method = model.predict(coefficients)[0]

        return jsonify({
            "recommended_method": method,
            "explanation": f"La méthode {method} a été recommandée en fonction des caractéristiques du polynôme."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Initialisation des logs
    logging.basicConfig(level=logging.INFO)

    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    logging.info(f"Démarrage du service {SERVICE_NAME} sur le port {SERVICE_PORT}.")
    app.run(host="0.0.0.0", port=SERVICE_PORT)
