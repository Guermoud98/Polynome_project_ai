import logging
import threading
import time

import requests
from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "graph-service"
SERVICE_PORT = 5004
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


@app.route('/plot', methods=['POST'])
def plot_graph():
    """
    Endpoint to plot the graph of a polynomial equation.
    """
    try:
        # Parse the request JSON
        data = request.get_json()
        equation = data.get("equation")
        variable = data.get("variable", "x")  # Default variable is 'x'

        if not equation:
            return jsonify({"error": "An equation must be provided."}), 400

        # Convert equation to a callable function
        equation = equation.replace("^", "**")
        x = np.linspace(-10, 10, 500)
        y = eval(equation)

        # Plot the graph
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, label=equation)
        plt.axhline(0, color='black', linewidth=0.8)
        plt.axvline(0, color='black', linewidth=0.8)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title("Polynomial Graph")
        plt.xlabel("x")
        plt.ylabel("f(x)")

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(buf, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    # Lancer le thread pour s'enregistrer auprès d'Eureka
    threading.Thread(target=register_with_eureka, daemon=True).start()

    # Démarrer l'application Flask
    logging.info(f"Démarrage du service graph sur le port {SERVICE_PORT}.")
    app.run(host='0.0.0.0', port=SERVICE_PORT)
