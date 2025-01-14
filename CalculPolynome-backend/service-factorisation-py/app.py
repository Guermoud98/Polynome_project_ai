from flask import Flask, request, jsonify
from factorisation_solver import advanced_factorization
import requests
import threading
import time
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "factorization-service"
SERVICE_PORT = 5000
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"
HOSTNAME = "127.0.0.1"  # Utilisation de localhost pour Eureka


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


@app.route('/factoriser', methods=['POST'])
def factorize_advanced():
    """
    Endpoint pour factoriser un polynôme.
    """
    try:
        # Lecture des données JSON envoyées par le client
        data = request.json
        equation = data.get('equation')
        variable = data.get('variable', 'x')  # Variable par défaut : 'x'

        if not equation:
            return jsonify({"success": False, "error": "L'équation est obligatoire."}), 400

        # Appel à la fonction de factorisation
        factorized_result = advanced_factorization(equation, variable)

        # Réponse au client
        return jsonify({
            "success": True,
            "original_equation": equation,
            "factorized_result": factorized_result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    app.run(host='0.0.0.0', port=SERVICE_PORT)
