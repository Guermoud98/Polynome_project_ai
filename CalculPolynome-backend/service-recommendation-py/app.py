from flask import Flask, request, jsonify
import joblib
import numpy as np
import sympy as sp

# Charger le modèle
model = joblib.load("method_classifier.pkl")

# Initialiser l'application Flask
app = Flask(__name__)

def parse_polynomial(polynomial):
    """
    Convertit un polynôme sous forme textuelle en une liste de coefficients normalisés à 6.
    Par exemple : "x^5 + x^2 + x" devient [1, 0, 0, 0, 1, 1].
    """
    x = sp.symbols('x')
    expr = sp.sympify(polynomial.replace("^", "**"))  # Convertir le polynôme en expression sympy
    coefficients = sp.Poly(expr, x).all_coeffs()  # Extraire les coefficients

    # Normaliser à une longueur de 6 (ajouter des zéros pour les degrés manquants)
    while len(coefficients) < 6:
        coefficients.insert(0, 0)

    # Si le degré est supérieur à 5, tronquer les coefficients
    coefficients = coefficients[-6:]

    return coefficients

@app.route("/recommend-method", methods=["POST"])
def recommend_method():
    """
    Endpoint pour recommander une méthode.
    Expects: {"polynomial": "x^5 + x^2 + x"}
    Returns: {"recommended_method": "Newton"}
    """
    data = request.get_json()
    polynomial = data.get("polynomial")

    try:
        # Convertir le polynôme en coefficients normalisés
        coefficients = parse_polynomial(polynomial)
        coefficients = np.array(coefficients).reshape(1, -1)

        # Log les coefficients
        print(f"Coefficients reçus : {coefficients}")

        # Faire une prédiction avec le modèle
        method = model.predict(coefficients)[0]

        # Log la méthode recommandée
        print(f"Méthode recommandée : {method}")

        return jsonify({"recommended_method": method})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Test manuel
    test_polynomials = [
        "x^2 + 4*x + 4",  # Quadratique
        "x^5 + x^3 + x",  # Newton
        "5",              # Quadratique
        "x^5 + x^4 - x^3" # Newton
    ]

    for poly in test_polynomials:
        coeffs = parse_polynomial(poly)
        prediction = model.predict(np.array(coeffs).reshape(1, -1))[0]
        print(f"Polynôme : {poly}, Coefficients : {coeffs}, Méthode : {prediction}")

    # Lancer le serveur Flask
    app.run(host="0.0.0.0", port=5006)
