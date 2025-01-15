from flask import Flask, request, jsonify
import joblib
import numpy as np
import sympy as sp

# Charger le modèle et l'encodeur
model = joblib.load("method_classifier.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Initialiser l'application Flask
app = Flask(__name__)

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

@app.route("/recommend-method", methods=["POST"])
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
    app.run(host="0.0.0.0", port=5006)
