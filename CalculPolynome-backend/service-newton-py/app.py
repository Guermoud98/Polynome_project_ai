from flask import Flask, request, jsonify
from newton_solver import newton_method
from models import SessionLocal, NewtonResult
import requests
import threading
import time
import logging

# Initialisation des logs
logging.basicConfig(level=logging.INFO)

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "newton-service"
SERVICE_PORT = 5001
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


@app.route('/newton', methods=['POST'])
def solve_with_newton():
    try:
        logging.info("Requête reçue pour résoudre avec Newton.")

        # Lecture des données envoyées par le client (format JSON)
        data = request.get_json()
        logging.info(f"Données reçues : {data}")

        equation = data.get("equation")  # Récupération de l'équation
        variable = data.get("variable", "x")  # Nom de la variable (par défaut : 'x')
        initial_guess = data.get("initial_guess", 0)  # Estimation initiale
        tolerance = data.get("tolerance", 1e-7)  # Tolérance pour la convergence
        max_iterations = data.get("max_iterations", 100)  # Nombre maximum d'itérations

        # Vérification des données obligatoires
        if not equation or variable is None:
            return jsonify({
                "error": "L'équation et la variable sont obligatoires.",
                "success": False
            }), 400

        # Appel de la méthode de Newton
        result = newton_method(equation, variable, float(initial_guess), float(tolerance), int(max_iterations))

        # Enregistrement du résultat dans la base de données
        session = SessionLocal()
        try:
            newton_result = NewtonResult(
                equation=equation,
                solution=result["solution"],
                iterations=result["iterations"],
                success="True" if result["success"] else "False"
            )
            session.add(newton_result)  # Ajout du résultat à la session
            session.commit()  # Validation de la transaction
        finally:
            session.close()

        # Retourner le résultat au client
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Erreur dans solve_with_newton : {str(e)}")
        # En cas d'erreur
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


if __name__ == '__main__':
    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    logging.info("Démarrage du service Newton sur le port 5001.")
    app.run(host='0.0.0.0', port=SERVICE_PORT)
