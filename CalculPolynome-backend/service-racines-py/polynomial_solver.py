from sympy import symbols, solve, simplify
from models import SessionLocal, PolynomialRoots

def find_roots(equation, variable):
    try:
        # Définition de la variable symbolique
        x = symbols(variable)

        # Simplification de l'équation
        simplified_eq = simplify(equation)

        # Calcul des racines
        roots = solve(simplified_eq, x)

        # Arrondir les racines à 2 décimales
        rounded_roots = [str(round(float(root), 2)) if root.is_real else str(root) for root in roots]

        # Stockage des données dans la bd
        session = SessionLocal()
        polynomial = PolynomialRoots(equation=equation, roots=", ".join(rounded_roots))
        session.add(polynomial)
        session.commit()
        session.close()

        # Retourner les racines
        return {
            "roots": rounded_roots,
            "original_equation": equation,
            "success": True
        }
    except Exception as e:
        return {
            "error": f"Erreur lors du calcul des racines : {str(e)}",
            "success": False
        }
