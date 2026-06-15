"""
Parser module for polynomial-explorer.

Handles flexible user input:
- String like "2x^3 - 3x^2 + 5", "x^2 - 1", "-0.5x^4 + x", "x"
- List/tuple/ndarray of coefficients in descending degree order: [2, -3, 0, 5]

Returns a sympy.Poly (univariate in symbol x). This keeps coefficients exact
where possible (rationals) and makes symbolic derivative / root finding easy.
"""

import re
from typing import Union, Sequence

import numpy as np
import sympy as sp


def parse_polynomial(input_data: Union[str, Sequence[float], Sequence[int]]) -> sp.Poly:
    """
    Parse a polynomial from either a human-readable string or a coefficient list.

    Parameters
    ----------
    input_data : str or sequence of numbers
        - String: "2x^3 - 3x^2 + 5", "x^2-x-6", "-0.5x^4", etc.
          Supports ^ or **, implicit multiplication (2x), spaces, leading +/-
        - Sequence: [a_n, a_{n-1}, ..., a_1, a_0]  (highest power first)

    Returns
    -------
    sympy.Poly
        A univariate polynomial in the symbol x.

    Raises
    ------
    ValueError
        If input cannot be interpreted as a polynomial.
    """
    x = sp.symbols('x')

    if isinstance(input_data, str):
        return _parse_string(input_data, x)
    elif isinstance(input_data, (list, tuple, np.ndarray)):
        return _parse_coeffs(input_data, x)
    else:
        raise ValueError(
            "Input must be a string (e.g. '2x^3-3x^2+5') or a list of coefficients "
            "in descending degree order (e.g. [2, -3, 0, 5])."
        )


def _parse_string(s: str, x: sp.Symbol) -> sp.Poly:
    """Use SymPy's parser with student-friendly transformations."""
    if not s or not s.strip():
        raise ValueError("Empty polynomial string.")

    # Normalize common student input variants
    s = s.strip()
    # convert ^ to ** for safety (convert_xor also does this)
    s = s.replace('^', '**')

    # SymPy's powerful parser with implicit multiplication and xor conversion
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication_application,
        convert_xor,
    )

    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    try:
        expr = parse_expr(s, transformations=transformations, local_dict={})
    except Exception as exc:
        raise ValueError(f"Could not parse polynomial string '{s}': {exc}") from exc

    try:
        poly = sp.Poly(expr, x, domain="QQ")
    except sp.PolynomialError:
        # Fall back to allowing floats / complex coeffs if QQ fails
        poly = sp.Poly(expr, x, domain="CC")

    # Remove zero terms for cleanliness (Poly already does this internally)
    return poly


def _parse_coeffs(coeffs: Sequence, x: sp.Symbol) -> sp.Poly:
    """Convert a list of coefficients (high degree first) into a Poly."""
    if len(coeffs) == 0:
        raise ValueError("Coefficient list cannot be empty.")

    # Convert to sympy numbers, preserving rationals when possible
    sympy_coeffs = []
    for c in coeffs:
        if isinstance(c, (int, np.integer)):
            sympy_coeffs.append(sp.Integer(int(c)))
        elif isinstance(c, (float, np.floating)):
            # Use Rational when it is close to a simple fraction
            rat = sp.Rational(c).limit_denominator(10000)
            sympy_coeffs.append(rat if abs(float(rat) - float(c)) < 1e-12 else sp.Float(c))
        else:
            sympy_coeffs.append(sp.sympify(c))

    # sp.Poly.from_list expects highest degree first
    poly = sp.Poly.from_list(sympy_coeffs, x)

    # If all coeffs are zero, still valid (zero polynomial)
    return poly


def coeffs_to_string(coeffs: Sequence[float], var: str = "x") -> str:
    """
    Convert a coefficient list (highest first) into a clean human string.
    Useful for round-tripping or display.
    """
    if len(coeffs) == 0:
        return "0"

    terms = []
    degree = len(coeffs) - 1

    for i, c in enumerate(coeffs):
        power = degree - i
        c = float(c)
        if abs(c) < 1e-12:
            continue

        # coefficient part
        sign = "+" if c > 0 and terms else ("-" if c < 0 else "")
        abs_c = abs(c)

        if power == 0:
            coeff_str = f"{abs_c:g}"
        elif abs_c == 1.0:
            coeff_str = "" if power > 0 else "1"
        else:
            coeff_str = f"{abs_c:g}"

        # variable part
        if power == 0:
            var_str = ""
        elif power == 1:
            var_str = var
        else:
            var_str = f"{var}^{power}"

        term = f"{sign}{coeff_str}{var_str}".strip()
        # Clean up "+-" or leading +
        if term.startswith("+"):
            term = term[1:]
        terms.append(term)

    if not terms:
        return "0"

    result = " ".join(terms)
    # Fix leading minus if first term negative
    if coeffs[0] < 0 and result.startswith("- "):
        result = "-" + result[2:]
    return result.strip()
