"""
High-level convenience API for polynomial-explorer.

This module ties together parsing, analysis, and visualization into
a single easy-to-use function that students (and instructors) can call
from scripts, notebooks, or the command line.

Primary entry point: explore()
"""

from typing import Union, Sequence, Optional
import sympy as sp

from .parser import parse_polynomial
from .analysis import (
    analyze_polynomial,
    PolynomialAnalysis,
    format_analysis_summary,
)
from .visualization import plot_polynomial


def explore(
    polynomial: Union[str, Sequence[float], Sequence[int]],
    show_plot: bool = True,
    print_summary: bool = True,
    save_plot: Optional[str] = None,
    **plot_kwargs,
) -> PolynomialAnalysis:
    """
    One-shot educational exploration of a polynomial.

    This is the function most users will call.

    Parameters
    ----------
    polynomial : str or list of coefficients
        Examples:
            "2x^3 - 3x^2 + 5"
            "x^2 - 1"
            "(x-1)^2*(x+3)"     # sympy parser handles expanded form too
            [1, -6, 11, -6]     # (x-1)(x-2)(x-3)
    show_plot : bool
        Display the rich matplotlib figure.
    print_summary : bool
        Print a clean formatted text summary to stdout.
    save_plot : str or None
        If given, save the figure to this filename (e.g. "my_poly.png").
    **plot_kwargs :
        Passed through to plot_polynomial (figsize, dpi, title, etc.).

    Returns
    -------
    PolynomialAnalysis
        The full structured analysis result. You can access:
            analysis.expression, .degree, .roots, .turning_points, etc.

    Examples
    --------
    >>> from polynomial_explorer import explore
    >>> analysis = explore("x^3 - 6x^2 + 11x - 6", show_plot=True)
    >>> explore([1, 0, -2], print_summary=False)   # x^2 - 2
    """
    # 1. Parse user input into a canonical sympy.Poly
    poly = parse_polynomial(polynomial)

    # 2. Perform complete mathematical analysis
    analysis = analyze_polynomial(poly)

    # 3. Print human-readable summary (very useful in notebooks + CLI)
    if print_summary:
        print(format_analysis_summary(analysis))

    # 4. Generate the beautiful educational visualization
    if show_plot or save_plot:
        plot_polynomial(
            poly,
            analysis=analysis,
            save_path=save_plot,
            show=show_plot,
            **plot_kwargs,
        )

    return analysis


def explore_many(
    polynomials: list,
    show_each: bool = True,
    **kwargs,
) -> list:
    """
    Explore a list of polynomials in sequence.
    Great for classroom demos or quick comparisons.
    """
    results = []
    for p in polynomials:
        print("\n" + "=" * 60)
        print(f"Exploring: {p}")
        print("=" * 60)
        res = explore(p, show_plot=show_each, **kwargs)
        results.append(res)
    return results
