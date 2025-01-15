import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
#*********/*/*/*/*/*/*/*/*
def generate_training_data(num_samples=1000):
    """
    Génère des données synthétiques pour entraîner un modèle de machine learning.

    :param num_samples: Nombre d'échantillons à générer.
    :return: Deux tableaux numpy:
             - X : Les caractéristiques des polynômes (coefficients, degré, etc.).
             - y : Les étiquettes (type de question à générer).
    """
    X = []  # Liste pour stocker les caractéristiques des polynômes.
    y = []  # Liste pour stocker les étiquettes associées.

    for _ in range(num_samples):
        # Générer aléatoirement 10 coefficients entre -10 et 10 pour représenter un polynôme
        coefficients = np.random.randint(-10, 10, size=10)

        # Calculer les caractéristiques :
        degree = len(coefficients) - np.count_nonzero(coefficients == 0) - 1  # Degré du polynôme.
        num_nonzero = np.count_nonzero(coefficients)  # Nombre de coefficients non nuls.
        max_coefficient = np.max(np.abs(coefficients))  # Coefficient absolu maximum.

        # Préparer la liste des caractéristiques (10 coefficients + 3 propriétés supplémentaires).
        features = list(coefficients) + [degree, num_nonzero, max_coefficient]

        # Déterminer l'étiquette en fonction du degré du polynôme.
        if degree <= 2:
            label = "Quadratique"  # Polynômes de degré ≤ 2.
        elif degree == 3:
            label = "Racines"  # Polynômes de degré 3.
        elif degree >= 4:
            label = "Factorisation"  # Polynômes de degré ≥ 4.
        else:
            label = "Newton"  # Cas spéciaux ou erreur.

        # Ajouter les caractéristiques et l'étiquette aux listes X et y.
        X.append(features)
        y.append(label)

    # Convertir les listes Python en tableaux numpy pour une utilisation efficace.
    return np.array(X), np.array(y)

# Générer des données pour entraîner le modèle.
X, y = generate_training_data(num_samples=2000)

# Diviser les données en ensembles d'entraînement (80%) et de test (20%).
# Cela permet d'entraîner le modèle sur une partie des données et de tester ses performances sur des données inconnues.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer un modèle RandomForestClassifier :
# - n_estimators=100 : Le nombre d'arbres dans la forêt.
# - max_depth=10 : La profondeur maximale des arbres pour limiter la complexité.
# - random_state=42 : Garde les résultats reproductibles.
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Entraîner le modèle sur l'ensemble d'entraînement.
model.fit(X_train, y_train)

# Effectuer des prédictions sur l'ensemble de test.
y_pred = model.predict(X_test)

# Évaluer les performances du modèle :
# - Affiche un rapport de classification contenant des métriques comme précision, rappel et f1-score.
print("Rapport de classification :")
print(classification_report(y_test, y_pred))

# Sauvegarder le modèle entraîné dans un fichier .pkl pour une utilisation future dans l'application Flask.
joblib.dump(model, "quiz_question_model.pkl")
print("Modèle sauvegardé dans 'quiz_question_model.pkl'")
