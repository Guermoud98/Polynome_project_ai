from sympy import symbols, Eq, solve
from models import SessionLocal, QuadraticEquation

def resolution_quadratique(a, b, c):
    try:
        if a == 0:
            raise ValueError("Ce n'est pas une équation quadratique, car a = 0.")

        # Définition de la variable symbolique x
        x = symbols('x')

        # Construction de l'équation
        equation = Eq(a * x**2 + b * x + c, 0)

        # Résolution de l'équation
        solutions = solve(equation, x)

        # Formatage des solutions avec un arrondi à 2 chiffres après la virgule
        roots = [round(float(solution), 2) for solution in solutions]

        # Stockage des résultats dans la base de données
        session = SessionLocal()
        quadratic_equation = QuadraticEquation(
            a=a,
            b=b,
            c=c,
            equation=f"{a}x^2 + {b}x + {c} = 0",
            roots=", ".join(map(str, roots))  # Conversion des racines en chaînes
        )
        session.add(quadratic_equation)
        session.commit()
        session.close()

        return {
            "equation": f"{a}x^2 + {b}x + {c} = 0",
            "roots": roots,  # Liste des racines arrondies
            "success": True
        }
    except Exception as e:
        return {
            "error": f"Erreur lors de la résolution : {e}",
            "success": False
        }
