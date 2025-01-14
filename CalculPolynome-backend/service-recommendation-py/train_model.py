import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Générer des données équilibrées
def generate_data(num_samples=100):
    X = []
    y = []
    for i in range(num_samples):
        coefficients = np.random.randint(-10, 10, size=6)  # 6 coefficients
        if i < num_samples // 2:
            coefficients[0] = 0  # Quadratique : pas de terme de degré 5
            y.append("Quadratique")
        else:
            coefficients[0] = np.random.randint(1, 10)  # Newton : degré 5 présent
            y.append("Newton")
        X.append(coefficients)
    return np.array(X), np.array(y)

# Générer les données
X, y = generate_data(200)

# Diviser en données d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle
model = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
model.fit(X_train, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Sauvegarder le modèle
joblib.dump(model, "method_classifier.pkl")
print("Modèle sauvegardé dans 'method_classifier.pkl'")
