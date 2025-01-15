import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier  # XGBoost
import joblib

def generate_data(num_samples=2000):
    """
    Génère des données équilibrées pour les classes Quadratique et Newton.
    """
    X = []
    y = []
    for i in range(num_samples):
        coefficients = np.zeros(10)  # Initialise un tableau de coefficients de degré 10

        if i < num_samples // 2:  # Quadratique
            coefficients[8] = np.random.randint(-10, 10)  # Terme de degré 2
            coefficients[9] = np.random.randint(-10, 10)  # Terme constant
            y.append("Quadratique")
        else:  # Newton
            coefficients[0] = np.random.randint(1, 10)  # Terme de degré 5
            coefficients[3] = np.random.randint(-10, 10)  # Terme de degré 2
            coefficients[9] = np.random.randint(-10, 10)  # Terme constant
            y.append("Newton")

        # Ajouter des caractéristiques supplémentaires
        num_nonzero = np.count_nonzero(coefficients)
        max_coefficient = np.max(coefficients)  # Maximum des coefficients
        coefficients = np.append(coefficients, [num_nonzero, max_coefficient])  # Ajouter des caractéristiques

        X.append(coefficients)

    return np.array(X), np.array(y)

# Générer les données
X, y = generate_data(num_samples=3000)

# Encoder les étiquettes
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Diviser en données d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle Gradient Boosting (XGBoost)
model = XGBClassifier(n_estimators=500, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test)
print("Rapport de classification :")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Sauvegarder le modèle et l'encodeur
joblib.dump(model, "method_classifier.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")  # Sauvegarde du label encoder
print("Modèle sauvegardé dans 'method_classifier.pkl'")
print("Encodeur sauvegardé dans 'label_encoder.pkl'")
