"""
Command-line interface entry point.

Allows:
    python -m polynomial_explorer "2x^3 - x + 1"
    python -m polynomial_explorer --interactive
    poly-explore "x^2-4"          (after pip install -e .)

Also works nicely in educational demos.
"""

import argparse
import sys

from .explorer import explore
from .parser import parse_polynomial


def main():
    parser = argparse.ArgumentParser(
        prog="polynomial-explorer",
        description="Explore polynomials: roots, multiplicity, end behavior, turning points, and beautiful plots.",
    )
    parser.add_argument(
        "polynomial",
        nargs="?",
        help='Polynomial as string, e.g. "2x^3 - 3x^2 + 5" or "x^2-1". '
             'If omitted and --interactive is not used, a demo polynomial is shown.',
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode: enter polynomials one after another.",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Only print the analysis summary (no matplotlib window).",
    )
    parser.add_argument(
        "--save",
        metavar="PATH",
        help="Save the plot to a file (e.g. --save output.png).",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run a short series of built-in educational examples.",
    )

    args = parser.parse_args()

    if args.examples:
        _run_examples(show_plot=not args.no_plot)
        return

    if args.interactive:
        _run_interactive(show_plot=not args.no_plot)
        return

    if args.polynomial:
        poly_str = args.polynomial
    else:
        # Friendly default demo
        poly_str = "x^3 - 6x^2 + 11x - 6"
        print(f"No polynomial given — showing demo: p(x) = {poly_str}\n")

    try:
        explore(
            poly_str,
            show_plot=not args.no_plot,
            save_plot=args.save,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _run_interactive(show_plot: bool = True):
    print("Polynomial Explorer — Interactive Mode")
    print("Enter a polynomial (e.g. 2x^3-3x^2+5) or 'q' to quit.\n")
    while True:
        try:
            user = input("poly> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user or user.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            break

        try:
            explore(user, show_plot=show_plot, print_summary=True)
        except Exception as exc:
            print(f"  Could not analyze: {exc}")


def _run_examples(show_plot: bool = True):
    """A curated set of polynomials that beautifully illustrate key concepts."""
    from .explorer import explore_many

    examples = [
        "x^3 - 6x^2 + 11x - 6",           # three distinct real roots
        "(x-2)^2*(x-5)",                  # double root + single (touch + cross)
        "x^4 - 5x^2 + 4",                 # even degree, four real roots
        "x^2 + 1",                        # no real roots, complex pair
        "x^3 - x",                        # inflection at 0, two turning points
        "-2x^3 + 3x^2 + 1",               # negative leading coeff + odd degree
        "x^5 - 3x^3 + 2x",                # higher odd degree
    ]

    print("Running built-in educational examples...\n")
    explore_many(examples, show_each=show_plot)


if __name__ == "__main__":
    main()
