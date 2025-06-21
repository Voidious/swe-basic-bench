# Task: Simple Calculator

Your task is to implement a simple calculator in Python. The calculator should be able to perform addition, subtraction, multiplication, and division.

## Requirements

1.  Create a Python file named `calculator.py` inside the current directory (`solution/`).
2.  Implement a class named `Calculator`.
3.  The `Calculator` class should have the following methods:
    -   `add(self, a, b)`: Returns the sum of `a` and `b`.
    -   `subtract(self, a, b)`: Returns the difference between `a` and `b`.
    -   `multiply(self, a, b)`: Returns the product of `a` and `b`.
    -   `divide(self, a, b)`: Returns the result of `a` divided by `b`.
4.  The `divide` method should handle division by zero by raising a `ValueError`.

## Verification

To verify your solution, run the tests located in the `../verifier/` directory. From within the `solution/` directory, you can run the tests using `pytest`.

First you will need to install pytest:
`pip install pytest`

Then, to run the verifier, execute the following command from the root of the `swe-basic-bench` directory:
`pytest tasks/simple-calculator/verifier/test_calculator.py`

Your goal is to make all the tests pass. 