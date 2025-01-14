from sympy import symbols, diff, lambdify, sympify

# Fonction pour résoudre une équation avec la méthode de Newton
def newton_method(equation, variable, initial_guess, tolerance=1e-7, max_iterations=100):
    try:
        # Remplacer ^ par ** pour compatibilité avec SymPy
        equation = equation.replace("^", "**")
        x = symbols(variable)  # Définir la variable symbolique
        equation = sympify(equation)  # Convertir l'équation en objet SymPy

        # Calcul de la dérivée de l'équation
        derivative = diff(equation, x)

        # Conversion de l'équation et de la dérivée en fonctions Python évaluables
        f = lambdify(x, equation)  # Fonction f(x)
        f_prime = lambdify(x, derivative)  # Fonction f'(x)

        # Initialisation de la méthode de Newton
        current_guess = initial_guess
        for iteration in range(max_iterations):
            # Calcul de la valeur de la fonction et de sa dérivée au point actuel
            f_value = f(current_guess)
            f_prime_value = f_prime(current_guess)

            # Éviter la division par zéro
            if abs(f_prime_value) < 1e-12:
                raise ValueError("La dérivée est proche de zéro, la méthode de Newton ne peut pas continuer.")

            # Calcul de la prochaine estimation
            next_guess = current_guess - f_value / f_prime_value

            # Vérification de la convergence
            if abs(next_guess - current_guess) < tolerance:
                return {
                    "solution": round(next_guess, 2),  # La solution arrondie à 2 décimales
                    "iterations": iteration + 1,  # Nombre d'itérations effectuées
                    "success": True  # Indicateur de succès
                }

            current_guess = next_guess  # Mise à jour de l'estimation

        # Si la méthode n'a pas convergé
        raise ValueError("La méthode de Newton n'a pas convergé après le nombre maximum d'itérations.")
    except Exception as e:
        raise ValueError(f"Erreur lors de la résolution par Newton : {e}")
