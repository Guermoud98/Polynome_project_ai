from flask import Flask, request, jsonify
from quadratique_solver import resolution_quadratique
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
SERVICE_NAME = "quadratic-service"
SERVICE_PORT = 5003
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


@app.route('/quadratique', methods=['POST'])
def resolve_quadratic():
    try:
        # Lecture des données envoyées dans la requête
        data = request.json
        a = data.get('a')
        b = data.get('b')
        c = data.get('c')

        if a is None or b is None or c is None:
            return jsonify({
                "error": "Les paramètres 'a', 'b' et 'c' sont requis.",
                "success": False
            }), 400

        # Appel à la fonction de résolution
        result = resolution_quadratique(float(a), float(b), float(c))

        # Arrondir les solutions à deux décimales
        if "roots" in result:
            result["roots"] = [round(root, 2) for root in result["roots"]]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": f"Erreur lors de la résolution : {e}",
            "success": False
        }), 500


if __name__ == '__main__':
    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    logging.info(f"Démarrage du service Quadratique sur le port {SERVICE_PORT}.")
    app.run(host='0.0.0.0', port=SERVICE_PORT)
