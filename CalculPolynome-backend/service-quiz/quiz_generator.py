import sympy as sp

def generate_question_and_solution(polynomial, question_type):
    """
    Génère une question mathématique et sa solution avec une explication détaillée.

    :param polynomial: (str) Le polynôme en entrée, sous forme de chaîne de caractères.
    :param question_type: (str) Le type de question à générer (Factorisation, Racines, Quadratique, Newton).
    :return: (dict) Un dictionnaire contenant :
             - "question" : La question générée.
             - "solution" : La solution associée.
             - "explanation" : Une explication détaillée pour la solution.
    """
    # Définir la variable symbolique utilisée dans les polynômes
    x = sp.symbols('x')

    # Nettoyer le format du polynôme pour le rendre compatible avec sympy
    sanitized_polynomial = polynomial.replace("^", "**").replace(" ", "")

    try:
        # Convertir le polynôme en une expression mathématique interprétable par sympy
        expr = sp.sympify(sanitized_polynomial)

        # Générer la question en fonction du type demandé
        if question_type == "Factorisation":
            # Factoriser le polynôme
            factors = sp.factor(expr)
            question = f"Factorisez le polynôme : {sp.pretty(expr)}"
            solution = str(factors).replace("**", "^")  # Rendre l'expression lisible pour l'utilisateur

            # Fournir une explication détaillée
            explanation = (
                f"Pour factoriser le polynôme {polynomial} :\n"
                f"1. On identifie les racines en résolvant {polynomial} = 0.\n"
                f"2. Les racines permettent de construire les facteurs.\n"
                f"Le résultat est : {solution}."
            )

        elif question_type == "Racines":
            # Trouver les racines du polynôme
            roots = sp.solveset(expr, x, domain=sp.S.Reals)
            question = f"Trouvez les racines du polynôme : {sp.pretty(expr)}"
            solution = str(roots).replace("**", "^")  # Rendre les racines lisibles

            # Fournir une explication détaillée
            explanation = (
                f"Pour trouver les racines du polynôme {polynomial} :\n"
                f"1. On résout {polynomial} = 0.\n"
                f"Les racines trouvées sont : {roots}."
            )

        elif question_type == "Quadratique":
            # Résoudre une équation quadratique (degré ≤ 2)
            solution = sp.solve(expr, x)  # Trouver les solutions exactes
            question = f"Résolvez le polynôme quadratique : {sp.pretty(expr)} = 0"

            # Fournir une explication détaillée
            explanation = (
                f"Pour résoudre le polynôme {polynomial} :\n"
                f"1. On applique la formule quadratique (ou équivalent).\n"
                f"Les solutions sont : {solution}."
            )

        elif question_type == "Newton":
            # Approximation des racines en utilisant la méthode de Newton
            roots = sp.nsolve(expr, x, [0, 1])  # Newton nécessite une estimation initiale
            question = f"Utilisez la méthode de Newton pour approximer les racines de : {sp.pretty(expr)}"
            solution = str(roots).replace("**", "^")  # Formatage pour l'utilisateur

            # Fournir une explication détaillée
            explanation = (
                f"Pour approximer les racines de {polynomial} avec la méthode de Newton :\n"
                f"1. On choisit une estimation initiale.\n"
                f"2. On utilise des itérations pour affiner les racines.\n"
                f"La solution approximée est : {solution}."
            )

        else:
            # Gestion des types de questions non supportés
            raise ValueError("Type de question non pris en charge.")

        # Retourner les résultats sous forme de dictionnaire
        return {
            "question": question,
            "solution": solution,
            "explanation": explanation
        }

    except Exception as e:
        # Gérer les erreurs qui pourraient survenir (exemple : polynôme mal formaté)
        raise ValueError(f"Erreur lors de la génération du quiz : {e}")
