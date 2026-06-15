"""
Educational demonstration script for polynomial-explorer.

Run this to see several carefully chosen polynomials that highlight
different important mathematical phenomena:

- Distinct real roots
- Repeated roots (multiplicity > 1) and how the graph "touches"
- Polynomials with no real roots (complex conjugate pairs)
- Inflection points and turning points
- Effect of negative leading coefficients and even/odd degree on end behavior

Usage:
    python examples/demo.py
    python examples/demo.py --no-show          # just print summaries
    python -m polynomial_explorer --examples   # same set via CLI
"""

import sys
from pathlib import Path

# Make the package importable when running the demo directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from polynomial_explorer import explore, explore_many


def main(show: bool = True):
    print("\n" + "=" * 72)
    print("POLYNOMIAL EXPLORER — EDUCATIONAL DEMOS")
    print("=" * 72)
    print("\nEach example is chosen to illustrate a specific concept.\n")

    # ------------------------------------------------------------------
    # 1. Three distinct real roots (nice cubic)
    # ------------------------------------------------------------------
    print("\n[1] Simple cubic with three distinct real roots")
    print("    p(x) = x³ - 6x² + 11x - 6   = (x-1)(x-2)(x-3)")
    print("    Concepts: degree 3, positive lead → -∞ to +∞, three crossings of x-axis\n")
    explore("x^3 - 6x^2 + 11x - 6", show_plot=show)

    # ------------------------------------------------------------------
    # 2. Repeated root — multiplicity teaches "touching"
    # ------------------------------------------------------------------
    print("\n[2] Double root + single root")
    print("    p(x) = (x-2)²(x-5)   = x³ - 9x² + 24x - 20")
    print("    Concepts: multiplicity 2 root touches and turns back (even multiplicity),\n"
          "              multiplicity 1 crosses. Turning point at the double root.\n")
    explore("(x-2)^2*(x-5)", show_plot=show)

    # ------------------------------------------------------------------
    # 3. No real roots — only complex conjugate pair
    # ------------------------------------------------------------------
    print("\n[3] Quadratic with no real roots (complex conjugate pair)")
    print("    p(x) = x² + 1")
    print("    Concepts: positive even degree → both ends +∞, never crosses x-axis,\n"
          "              roots are purely imaginary ±i. Look at the complex plane plot!\n")
    explore("x^2 + 1", show_plot=show)

    # ------------------------------------------------------------------
    # 4. Even degree, four real roots, negative leading coefficient
    # ------------------------------------------------------------------
    print("\n[4] Quartic with four real roots and negative leading coefficient")
    print("    p(x) = x⁴ - 5x² + 4   = (x²-1)(x²-4) = (x-2)(x-1)(x+1)(x+2)")
    print("    Concepts: even degree + negative lead → both ends go to -∞,\n"
          "              W shape with three turning points.\n")
    explore("x^4 - 5x^2 + 4", show_plot=show)

    # ------------------------------------------------------------------
    # 5. Inflection point at x=0 (classic x³ - x)
    # ------------------------------------------------------------------
    print("\n[5] Cubic with an inflection point")
    print("    p(x) = x³ - x   = x(x-1)(x+1)")
    print("    Concepts: odd degree, positive lead. At x=0 the derivative is also zero\n"
          "              but p''(0)=0 → inconclusive (true inflection point).\n"
          "              The graph crosses the x-axis but is momentarily flat.\n")
    explore("x^3 - x", show_plot=show)

    # ------------------------------------------------------------------
    # 6. Negative leading coefficient, odd degree (end behavior flip)
    # ------------------------------------------------------------------
    print("\n[6] Negative leading coefficient (odd degree)")
    print("    p(x) = -2x³ + 3x² + 1")
    print("    Concepts: as x → -∞, p(x) → +∞ ; as x → +∞, p(x) → -∞\n"
          "              (arrows on the plot point the opposite way from the usual cubic).\n")
    explore("-2x^3 + 3x^2 + 1", show_plot=show)

    # ------------------------------------------------------------------
    # 7. Higher degree (quintic) — more roots and turning points possible
    # ------------------------------------------------------------------
    print("\n[7] Quintic (degree 5) with several real roots")
    print("    p(x) = x⁵ - 3x³ + 2x")
    print("    Concepts: degree 5 (odd) can have up to 5 real roots and 4 turning points.\n"
          "              End behavior still dominated by the leading term.\n")
    explore("x^5 - 3x^3 + 2x", show_plot=show)

    print("\n" + "=" * 72)
    print("Demo complete. Try your own polynomials!")
    print("    python main.py \"your polynomial here\"")
    print("    python -m polynomial_explorer --interactive")
    print("=" * 72 + "\n")


if __name__ == "__main__":
    show = "--no-show" not in sys.argv and "-n" not in sys.argv
    main(show=show)
