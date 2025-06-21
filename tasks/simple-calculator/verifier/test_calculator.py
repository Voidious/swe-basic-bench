import pytest
import sys
import os

# Add the solution directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../solution')))

from calculator import Calculator

@pytest.fixture
def calculator():
    """Returns a Calculator instance."""
    return Calculator()

def test_add(calculator):
    assert calculator.add(1, 2) == 3
    assert calculator.add(-1, 1) == 0
    assert calculator.add(-1, -1) == -2
    assert calculator.add(0, 0) == 0
    assert calculator.add(1.5, 2.5) == 4.0

def test_subtract(calculator):
    assert calculator.subtract(2, 1) == 1
    assert calculator.subtract(-1, 1) == -2
    assert calculator.subtract(-1, -1) == 0
    assert calculator.subtract(0, 0) == 0
    assert calculator.subtract(2.5, 1.5) == 1.0

def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-1, 3) == -3
    assert calculator.multiply(-1, -1) == 1
    assert calculator.multiply(0, 100) == 0
    assert calculator.multiply(1.5, 2) == 3.0

def test_divide(calculator):
    assert calculator.divide(6, 3) == 2
    assert calculator.divide(-6, 3) == -2
    assert calculator.divide(-6, -3) == 2
    assert calculator.divide(0, 1) == 0
    assert calculator.divide(5, 2) == 2.5

def test_divide_by_zero(calculator):
    with pytest.raises(ValueError):
        calculator.divide(1, 0) 