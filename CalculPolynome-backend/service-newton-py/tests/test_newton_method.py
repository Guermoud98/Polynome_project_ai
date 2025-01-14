import pytest
from unittest.mock import MagicMock, patch
from newton_solver import newton_method
from models import SessionLocal, NewtonResult

# Cas de test 1 : Test avec une équation valide
def test_newton_method_valid():
    equation = "x^2 - 4"
    variable = "x"
    initial_guess = 2.0

    result = newton_method(equation, variable, initial_guess)

    # Vérifications
    assert result["success"] is True
    assert result["solution"] == 2.0
    assert result["iterations"] > 0

# Cas de test 2 : Test d'une équation invalide
def test_newton_method_invalid_equation():
    equation = "invalid_equation"
    variable = "x"
    initial_guess = 1.0

    with pytest.raises(ValueError) as exc_info:
        newton_method(equation, variable, initial_guess)

    # Vérifier que l'erreur retournée est cohérente
    assert "Erreur lors de la résolution par Newton" in str(exc_info.value)

# Cas de test 3 : Test avec une dérivée proche de zéro
def test_newton_method_derivative_zero():
    equation = "x^3"
    variable = "x"
    initial_guess = 0.0

    with pytest.raises(ValueError) as exc_info:
        newton_method(equation, variable, initial_guess)

    # Vérifier que le bon message d'erreur est retourné
    assert "La dérivée est proche de zéro" in str(exc_info.value)

