"""
polynomial-explorer

An educational Python package for deeply understanding polynomials.

Core ideas demonstrated:
- Roots (real & complex) and their multiplicities
- End behavior determined by degree and leading coefficient
- Turning points found via the derivative + second derivative test
- Visual connection between algebraic structure and the graph

Quick start
-----------
from polynomial_explorer import explore

explore("2x^3 - 3x^2 + 5")
explore([1, -5, 6])          # x^2 - 5x + 6
"""

from .parser import parse_polynomial
from .analysis import (
    analyze_polynomial,
    PolynomialAnalysis,
    Root,
    TurningPoint,
    format_analysis_summary,
)
from .visualization import plot_polynomial
from .explorer import explore, explore_many

__all__ = [
    "explore",
    "explore_many",
    "parse_polynomial",
    "analyze_polynomial",
    "plot_polynomial",
    "PolynomialAnalysis",
    "Root",
    "TurningPoint",
    "format_analysis_summary",
]

__version__ = "0.1.0"
