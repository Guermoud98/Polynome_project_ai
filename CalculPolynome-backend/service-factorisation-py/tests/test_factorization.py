import pytest
from unittest.mock import MagicMock, patch
from factorisation_solver import advanced_factorization

# Cas de test 1 : Test d'une factorisation valide
def test_advanced_factorization_valid():
    equation = "x^2 - 4"
    variable = "x"

    # Simuler le stockage en base de données
    mock_session = MagicMock()
    with patch("factorisation_solver.SessionLocal", return_value=mock_session):
        result = advanced_factorization(equation, variable)

    assert result == "(x - 2)*(x + 2)"

# Cas de test 2 : Test d'une équation invalide
def test_advanced_factorization_invalid():
    equation = "invalid_equation"
    variable = "x"

    with pytest.raises(ValueError) as exc_info:
        advanced_factorization(equation, variable)

    assert "L'équation fournie n'est pas factorisable ou est invalide." in str(exc_info.value)


# Cas de test 3 : Test de la conversion de ** en ^
def test_advanced_factorization_conversion():
    equation = "x**2 - 4"
    variable = "x"

    # Simuler le stockage en base de données
    mock_session = MagicMock()
    with patch("factorisation_solver.SessionLocal", return_value=mock_session):
        result = advanced_factorization(equation, variable)

    assert result == "(x - 2)*(x + 2)"
