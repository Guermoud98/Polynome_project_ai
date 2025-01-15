import logging
import threading
import time

import requests
from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
import io
from sklearn.linear_model import LinearRegression # permet de créer un modèle linéaire pour prédire des valeurs continues
from sklearn.preprocessing import PolynomialFeatures #permet de transformer les caractéristiques d'entrée pour ajuster un modèle polynomial

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Configuration Eureka
EUREKA_SERVER = "http://localhost:8761/eureka/apps/"
SERVICE_NAME = "graph-service-predict"
SERVICE_PORT = 5010
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"
HOSTNAME = "127.0.0.1"  # Utilisation de localhost pour Eureka

# Load or initialize the machine learning model
poly_degree = 2
poly = PolynomialFeatures(degree=poly_degree)
model = LinearRegression()

# Example training data for the model
X_train = np.array([-3, -2, -1, 0, 1, 2, 3]).reshape(-1, 1)
y_train = np.array([-27, -8, -1, 0, 1, 8, 27])
X_poly = poly.fit_transform(X_train)
model.fit(X_poly, y_train)

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

@app.route('/predict-and-plot', methods=['POST'])
def predict_and_plot():
    """
    Endpoint to predict a polynomial equation and plot the graph.
    """
    try:
        # Parse the request JSON
        data = request.get_json()
        x_values = data.get("x_values")

        if not x_values:
            return jsonify({"error": "x_values must be provided."}), 400

        # Ensure x_values is a NumPy array
        x_values = np.array(x_values).reshape(-1, 1)

        # Predict using the trained model
        x_poly = poly.transform(x_values)
        y_pred = model.predict(x_poly)

        # Plot the graph
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_pred, color='red', label='Predicted Points')
        plt.plot(x_values, y_pred, label='Predicted Curve')
        plt.axhline(0, color='black', linewidth=0.8)
        plt.axvline(0, color='black', linewidth=0.8)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title("Predicted Polynomial Graph")
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
