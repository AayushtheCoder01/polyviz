"""
Analysis module for polynomial-explorer.

Pure mathematical logic (no plotting). Provides:

- Degree, leading coefficient
- End behavior description (text)
- All roots (real + complex) with exact multiplicity (via SymPy)
- Turning points (critical points) by solving p'(x) = 0
- Classification of turning points using second derivative test
- A clean, structured summary dictionary suitable for printing or further use

All functions work with a sympy.Poly for exactness where possible.
"""

from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any

import numpy as np
import sympy as sp


@dataclass
class Root:
    """A root with multiplicity. Value stored as complex for uniformity."""
    value: complex
    multiplicity: int

    @property
    def is_real(self) -> bool:
        return abs(self.value.imag) < 1e-10

    @property
    def real_value(self) -> float:
        return self.value.real if self.is_real else float("nan")


@dataclass
class TurningPoint:
    """A critical point (where p'(x) == 0)."""
    x: float
    y: float
    kind: str           # "local max", "local min", or "inflection / inconclusive"
    second_derivative: float


@dataclass
class PolynomialAnalysis:
    """Complete analysis result. Easy to print or serialize."""
    expression: str
    degree: int
    leading_coefficient: float
    end_behavior: str
    roots: List[Root]
    turning_points: List[TurningPoint]
    # Extra metadata
    is_zero_polynomial: bool = False


def analyze_polynomial(poly: sp.Poly) -> PolynomialAnalysis:
    """
    Perform full educational analysis of a univariate polynomial.

    Parameters
    ----------
    poly : sympy.Poly
        The polynomial (must be univariate).

    Returns
    -------
    PolynomialAnalysis
        Structured dataclass containing everything needed for display and plotting.
    """
    x = poly.gen

    if poly.is_zero:
        return PolynomialAnalysis(
            expression="0",
            degree=0,
            leading_coefficient=0.0,
            end_behavior="The zero polynomial is constant (p(x) = 0 for all x).",
            roots=[],
            turning_points=[],
            is_zero_polynomial=True,
        )

    # Basic info
    degree = int(poly.degree())
    lead_coeff = float(poly.LC())

    # Human-friendly expression string
    expr_str = _nice_expr_string(poly)

    # End behavior (purely from degree + sign of leading coefficient)
    end_behavior = _describe_end_behavior(degree, lead_coeff)

    # Roots with multiplicity (exact where possible)
    roots = _find_roots_with_multiplicity(poly)

    # Turning points via first derivative + second derivative classification
    turning_points = _find_turning_points(poly, x)

    return PolynomialAnalysis(
        expression=expr_str,
        degree=degree,
        leading_coefficient=lead_coeff,
        end_behavior=end_behavior,
        roots=roots,
        turning_points=turning_points,
    )


def _nice_expr_string(poly: sp.Poly) -> str:
    """Return a clean string representation, e.g. '2*x**3 - 3*x**2 + 5'."""
    # Use sympy's default but clean it up a little for students
    s = str(poly.as_expr())
    # Replace ** with ^ for familiarity, but keep * for clarity
    s = s.replace("**", "^")
    return s


def _describe_end_behavior(degree: int, lead: float) -> str:
    """
    Explain end behavior in plain English + limit notation.

    This is one of the most important big-picture ideas for students:
    the leading term dominates as |x| becomes large.
    """
    sign_lead = "positive" if lead > 0 else "negative"

    if degree % 2 == 0:
        if lead > 0:
            return (
                "Even degree with positive leading coefficient → both ends go to +∞.\n"
                "    As x → +∞, p(x) → +∞    and    As x → -∞, p(x) → +∞"
            )
        else:
            return (
                "Even degree with negative leading coefficient → both ends go to -∞.\n"
                "    As x → +∞, p(x) → -∞    and    As x → -∞, p(x) → -∞"
            )
    else:
        if lead > 0:
            return (
                "Odd degree with positive leading coefficient → from -∞ to +∞.\n"
                "    As x → -∞, p(x) → -∞    and    As x → +∞, p(x) → +∞"
            )
        else:
            return (
                "Odd degree with negative leading coefficient → from +∞ to -∞.\n"
                "    As x → -∞, p(x) → +∞    and    As x → +∞, p(x) → -∞"
            )


def _find_roots_with_multiplicity(poly: sp.Poly) -> List[Root]:
    """
    Return all roots (real and complex) with their algebraic multiplicities.

    Uses sympy.roots() which returns a dict {root: multiplicity} and tries to
    give exact algebraic answers (sqrt, etc.) when possible. We convert to
    complex for uniform handling in visualization and tables.
    """
    root_dict = sp.roots(poly.as_expr())
    roots: List[Root] = []

    for root_sym, mult in sorted(root_dict.items(), key=lambda kv: (float(sp.re(kv[0])), float(sp.im(kv[0])))):
        # Convert symbolic root to numeric complex
        try:
            val = complex(root_sym.evalf())
        except Exception:
            val = complex(float(sp.re(root_sym)), float(sp.im(root_sym)))

        roots.append(Root(value=val, multiplicity=int(mult)))

    return roots


def _find_turning_points(poly: sp.Poly, x: sp.Symbol) -> List[TurningPoint]:
    """
    Find turning points (local extrema / flat points) by solving p'(x) = 0.

    Classification uses the second derivative test:
        p''(c) > 0  → local minimum
        p''(c) < 0  → local maximum
        p''(c) ≈ 0  → inconclusive (inflection or higher-order flat point)
    """
    if poly.degree() < 1:
        return []

    p_prime = poly.diff(x)
    p_double_prime = p_prime.diff(x)

    # Critical points: solve p'(x) = 0
    crit_roots = sp.roots(p_prime.as_expr())

    turning_points: List[TurningPoint] = []

    for c_sym, _mult in crit_roots.items():
        # Numeric value of the critical point
        c = float(sp.N(c_sym))

        # y value
        y = float(sp.N(poly.subs(x, c_sym)))

        # Second derivative value at c
        ppp_val = float(sp.N(p_double_prime.subs(x, c_sym)))

        # Classify
        if abs(ppp_val) < 1e-9:
            kind = "inflection / inconclusive"
        elif ppp_val > 0:
            kind = "local min"
        else:
            kind = "local max"

        turning_points.append(
            TurningPoint(
                x=c,
                y=y,
                kind=kind,
                second_derivative=ppp_val,
            )
        )

    # Sort left to right by x
    turning_points.sort(key=lambda tp: tp.x)
    return turning_points


def format_analysis_summary(analysis: PolynomialAnalysis, max_width: int = 70) -> str:
    """
    Create a beautiful plain-text summary suitable for printing in terminal
    or notebooks. Uses simple aligned tables (no external dependencies).
    """
    lines = []
    lines.append("=" * max_width)
    lines.append("POLYNOMIAL ANALYSIS".center(max_width))
    lines.append("=" * max_width)
    lines.append("")

    # Equation
    lines.append(f"p(x) = {analysis.expression}")
    lines.append(f"Degree: {analysis.degree}")
    lines.append(f"Leading coefficient: {analysis.leading_coefficient:g}")
    lines.append("")

    # End behavior
    lines.append("END BEHAVIOR")
    lines.append("-" * 20)
    for line in analysis.end_behavior.split("\n"):
        lines.append(line)
    lines.append("")

    # Roots table
    lines.append("ROOTS (with multiplicity)")
    lines.append("-" * 20)
    if not analysis.roots:
        lines.append("  (none)")
    else:
        # header
        lines.append(f"  {'Root':<22} {'Multiplicity':>12} {'Type':>10}")
        lines.append("  " + "-" * 46)
        for r in analysis.roots:
            if r.is_real:
                root_str = f"{r.real_value:.10g}"
                rtype = "Real"
            else:
                root_str = f"{r.value.real:.6g} + {r.value.imag:.6g}i" if r.value.imag >= 0 else \
                           f"{r.value.real:.6g} - {abs(r.value.imag):.6g}i"
                rtype = "Complex"
            lines.append(f"  {root_str:<22} {r.multiplicity:>12} {rtype:>10}")
    lines.append("")

    # Turning points table
    lines.append("TURNING POINTS (critical points)")
    lines.append("-" * 20)
    if not analysis.turning_points:
        lines.append("  (none — e.g. strictly increasing/decreasing or degree < 2)")
    else:
        lines.append("  {:>14} {:>14} {:<22} {:>12}".format("x", "p(x)", "Kind", "p''(x) sign"))
        lines.append("  " + "-" * 66)
        for tp in analysis.turning_points:
            sign = "positive" if tp.second_derivative > 0 else ("negative" if tp.second_derivative < 0 else "≈ 0")
            lines.append(
                f"  {tp.x:>14.6g} {tp.y:>14.6g} {tp.kind:<22} {sign:>12}"
            )
    lines.append("")
    lines.append("=" * max_width)

    return "\n".join(lines)


def get_real_roots(analysis: PolynomialAnalysis) -> List[Root]:
    """Convenience filter for real roots only (useful for plotting)."""
    return [r for r in analysis.roots if r.is_real]


def get_complex_roots(analysis: PolynomialAnalysis) -> List[Root]:
    """Convenience filter for non-real roots."""
    return [r for r in analysis.roots if not r.is_real]
