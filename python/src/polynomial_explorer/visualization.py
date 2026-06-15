"""
Visualization module for polynomial-explorer.

Creates a rich, educational, publication-quality matplotlib figure that
helps students connect algebraic facts (roots, multiplicity, derivative zeros)
with the visual graph of the polynomial.

Layout (educational priorities):
  - Large main plot: smooth curve of p(x) on a carefully chosen real interval.
    * Real roots shown with prominent markers (size encodes multiplicity).
    * Turning points (critical points) shown with distinct markers + dashed
      projection lines to the axes.
    * End-behavior arrows + text annotations at the left and right edges.
    * Subtle info box with degree + leading coefficient + one-line end behavior.

  - Lower row of two supporting plots:
    1. Derivative p'(x): zeros of the derivative = turning points of p(x).
       This makes the relationship between p' and turning points crystal clear.
    2. Roots in the complex plane: all roots (real + complex) plotted as
       points in ℂ. Real roots lie on the horizontal axis and are drawn larger.
       This visually demonstrates that non-real roots come in conjugate pairs
       for polynomials with real coefficients.

Style: modern dark theme with high-contrast, colorblind-friendly accents.
Everything is extensively annotated so the picture itself teaches.
"""

from typing import Optional, Tuple, List
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D

from .analysis import PolynomialAnalysis, Root, TurningPoint, get_real_roots, get_complex_roots


# =============================================================================
# Public API
# =============================================================================

def plot_polynomial(
    poly: sp.Poly,
    analysis: Optional[PolynomialAnalysis] = None,
    title: Optional[str] = None,
    figsize: Tuple[float, float] = (15, 9),
    dpi: int = 140,
    save_path: Optional[str] = None,
    show: bool = True,
    num_points: int = 900,
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Create the full educational visualization for a polynomial.

    Parameters
    ----------
    poly : sympy.Poly
        The polynomial to visualize.
    analysis : PolynomialAnalysis, optional
        Pre-computed analysis. If None, it will be computed internally.
    title : str, optional
        Custom figure title. If None, a mathematical title is generated.
    figsize, dpi : figure size and resolution.
    save_path : str or None
        If provided, the figure is saved to this path (png/pdf/svg supported).
    show : bool
        Whether to call plt.show() at the end.
    num_points : int
        Number of sample points for the smooth curve (higher = smoother).

    Returns
    -------
    fig, axes
        The matplotlib Figure and array of Axes for further customization
        in Jupyter or scripts.
    """
    if analysis is None:
        from .analysis import analyze_polynomial
        analysis = analyze_polynomial(poly)

    x_sym = poly.gen

    # 1. Determine a good real-domain window that shows all important features
    x_min, x_max = _choose_x_window(analysis, poly, x_sym, margin_factor=0.65)

    # 2. Sample the polynomial smoothly
    x_vals = np.linspace(x_min, x_max, num_points)
    y_vals = _evaluate_poly_numpy(poly, x_sym, x_vals)

    # 3. Prepare derivative samples for the supporting plot
    p_prime = poly.diff(x_sym)
    y_prime_vals = _evaluate_poly_numpy(p_prime, x_sym, x_vals)

    # 4. Create the figure with a nice dark academic style
    plt.style.use("dark_background")
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="#0f111a")
    fig.patch.set_facecolor("#0f111a")

    # GridSpec: main plot on top (larger), two supporting plots below
    gs = fig.add_gridspec(
        2, 2,
        height_ratios=[2.35, 1.0],
        hspace=0.32,
        wspace=0.22,
        left=0.06, right=0.97, top=0.92, bottom=0.07,
    )

    ax_main = fig.add_subplot(gs[0, :])          # full-width top row
    ax_deriv = fig.add_subplot(gs[1, 0])
    ax_complex = fig.add_subplot(gs[1, 1])

    # =====================================================================
    # MAIN PLOT: p(x)
    # =====================================================================
    _setup_main_axis(ax_main, x_vals, y_vals, analysis, poly, x_sym, x_min, x_max)

    # Plot the smooth curve
    curve_color = "#00e5ff"
    ax_main.plot(
        x_vals, y_vals,
        color=curve_color,
        linewidth=2.8,
        label=r"$p(x)$",
        zorder=3,
        alpha=0.95,
    )

    # Mark real roots (large, prominent, size grows with multiplicity)
    real_roots = get_real_roots(analysis)
    _draw_real_roots(ax_main, real_roots, poly, x_sym)

    # Mark turning points + projection lines
    _draw_turning_points(ax_main, analysis.turning_points)

    # End behavior arrows + annotations (the "visual" part of end behavior)
    _add_end_behavior_arrows(ax_main, analysis, x_min, x_max)

    # Informational text box (degree, leading coeff, short end behavior)
    _add_info_box(ax_main, analysis)

    # Title
    if title is None:
        title = rf"Polynomial:  $p(x) = {sp.latex(poly.as_expr())}$"
    ax_main.set_title(title, fontsize=16, fontweight="bold", pad=12, color="white")

    ax_main.set_xlabel(r"$x$", fontsize=13)
    ax_main.set_ylabel(r"$p(x)$", fontsize=13)
    ax_main.legend(loc="upper left", framealpha=0.85, fontsize=10)

    # =====================================================================
    # SUPPORTING PLOT 1: p'(x) — why turning points happen
    # =====================================================================
    _plot_derivative(ax_deriv, x_vals, y_prime_vals, analysis, p_prime, x_sym)

    # =====================================================================
    # SUPPORTING PLOT 2: Roots in the complex plane
    # =====================================================================
    _plot_complex_roots_plane(ax_complex, analysis)

    # Overall figure title / caption
    fig.suptitle(
        "Educational view: function shape • derivative zeros • roots in ℂ",
        fontsize=11,
        color="#aaaaaa",
        y=0.015,
        style="italic",
    )

    if save_path:
        fig.savefig(save_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches="tight")
        print(f"Saved figure to {save_path}")

    if show:
        plt.show()

    return fig, np.array([ax_main, ax_deriv, ax_complex])


# =============================================================================
# Internal helpers — main plot construction
# =============================================================================

def _setup_main_axis(ax, x_vals, y_vals, analysis, poly, x_sym, x_min, x_max):
    """Styling and reference lines for the primary p(x) plot."""
    ax.set_facecolor("#161b2e")
    ax.grid(True, linestyle=":", alpha=0.35, color="#555555")
    for spine in ax.spines.values():
        spine.set_color("#444455")
        spine.set_linewidth(1.0)

    # Horizontal zero line (x-axis for roots)
    ax.axhline(0, color="#888888", linewidth=1.0, linestyle="-", alpha=0.6, zorder=1)

    # Nice symmetric or padded y limits
    y_min, y_max = float(np.min(y_vals)), float(np.max(y_vals))
    y_range = y_max - y_min if y_max != y_min else 1.0
    ax.set_ylim(y_min - 0.18 * y_range, y_max + 0.18 * y_range)
    ax.set_xlim(x_min, x_max)


def _draw_real_roots(ax, real_roots: List[Root], poly: sp.Poly, x_sym: sp.Symbol):
    """
    Draw real roots with size proportional to multiplicity.
    Also add a small multiplicity label for roots with mult >= 2.
    """
    if not real_roots:
        return

    root_color = "#ff5252"
    edge_color = "#ffffff"

    for root in real_roots:
        x_r = root.real_value
        y_r = 0.0
        # Size encodes multiplicity (min size 140, grows nicely)
        size = 140 + 85 * (root.multiplicity - 1)
        ax.scatter(
            [x_r], [y_r],
            s=size,
            c=root_color,
            edgecolors=edge_color,
            linewidths=1.6,
            zorder=5,
            marker="o",
            label=None,
        )

        # Small label for higher-multiplicity roots (educational)
        if root.multiplicity >= 2:
            label = f"mult = {root.multiplicity}"
            ax.annotate(
                label,
                xy=(x_r, y_r),
                xytext=(0, 18),
                textcoords="offset points",
                fontsize=9,
                color="#ffcccc",
                ha="center",
                va="bottom",
                fontweight="medium",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#2a1f1f", edgecolor="#ff5252", alpha=0.9),
                arrowprops=dict(arrowstyle="-", color="#ff8888", lw=0.8),
            )


def _draw_turning_points(ax, turning_points: List[TurningPoint]):
    """
    Draw turning points as prominent diamonds.
    Add dashed projection lines (vertical to x-axis, horizontal to y-axis).
    This helps students see the (x, p(x)) coordinates of local max/min.
    """
    if not turning_points:
        return

    tp_color = "#ffab40"
    for tp in turning_points:
        # Projection lines (very educational)
        ax.axvline(tp.x, color=tp_color, linestyle=":", linewidth=1.1, alpha=0.45, zorder=1)
        ax.axhline(tp.y, color=tp_color, linestyle=":", linewidth=1.1, alpha=0.35, zorder=1)

        # The marker itself
        ax.scatter(
            [tp.x], [tp.y],
            s=110,
            c=tp_color,
            edgecolors="#ffffff",
            linewidths=1.3,
            marker="D",
            zorder=6,
        )

        # Tiny label with kind
        short = tp.kind.replace("local ", "").replace("inflection / ", "")
        ax.annotate(
            short,
            xy=(tp.x, tp.y),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8,
            color="#ffe0b2",
            alpha=0.95,
        )


def _add_end_behavior_arrows(ax, analysis: PolynomialAnalysis, x_min: float, x_max: float):
    """
    Draw short but clear arrows at the left and right extremes of the plot
    that indicate whether p(x) is heading toward +∞ or -∞.

    This is the *visual* counterpart to the textual end-behavior description.
    """
    # Decide directions from the mathematical description
    deg = analysis.degree
    lead = analysis.leading_coefficient

    # As x → +∞ direction
    if deg % 2 == 0:
        right_dir = +1 if lead > 0 else -1
    else:
        right_dir = +1 if lead > 0 else -1

    # As x → -∞ direction (opposite for odd degree)
    if deg % 2 == 0:
        left_dir = right_dir
    else:
        left_dir = -right_dir

    # Place arrows just inside the current x limits, pointing outward
    x_left = x_min + 0.04 * (x_max - x_min)
    x_right = x_max - 0.04 * (x_max - x_min)

    y_range = ax.get_ylim()
    y_span = y_range[1] - y_range[0]
    arrow_len = 0.09 * y_span

    # Left arrow
    y_left = float(np.mean(y_range))  # neutral starting height
    _draw_arrow(ax, x_left, y_left, -1.0, left_dir * arrow_len, color="#a5d6a7")

    # Right arrow
    y_right = float(np.mean(y_range))
    _draw_arrow(ax, x_right, y_right, +1.0, right_dir * arrow_len, color="#a5d6a7")

    # Small textual end-behavior hints near the arrows
    left_text = "→ -∞" if left_dir < 0 else "→ +∞"
    right_text = "→ -∞" if right_dir < 0 else "→ +∞"

    ax.text(
        x_left - 0.02 * (x_max - x_min), y_left + left_dir * arrow_len * 0.7,
        left_text, fontsize=10, color="#a5d6a7", ha="right", va="center", fontweight="bold",
    )
    ax.text(
        x_right + 0.02 * (x_max - x_min), y_right + right_dir * arrow_len * 0.7,
        right_text, fontsize=10, color="#a5d6a7", ha="left", va="center", fontweight="bold",
    )


def _draw_arrow(ax, x, y, x_dir, y_delta, color="#a5d6a7", lw=2.2):
    """Small helper for a clean arrow annotation."""
    ax.annotate(
        "",
        xy=(x + x_dir * 0.06 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
            y + y_delta),
        xytext=(x, y),
        arrowprops=dict(
            arrowstyle="->",
            color=color,
            lw=lw,
            mutation_scale=14,
        ),
        zorder=4,
    )


def _add_info_box(ax, analysis: PolynomialAnalysis):
    """Compact facts box in the upper-right of the main plot."""
    lead_str = f"{analysis.leading_coefficient:g}"
    text = (
        f"Degree = {analysis.degree}\n"
        f"Leading coeff = {lead_str}\n"
        f"Real roots: {len([r for r in analysis.roots if r.is_real])}"
    )

    ax.text(
        0.98, 0.97,
        text,
        transform=ax.transAxes,
        fontsize=9.5,
        color="#e0e0e0",
        ha="right", va="top",
        family="monospace",
        bbox=dict(
            boxstyle="round,pad=0.45",
            facecolor="#1f243a",
            edgecolor="#4a4f6a",
            alpha=0.92,
        ),
        zorder=10,
    )


# =============================================================================
# Derivative subplot
# =============================================================================

def _plot_derivative(ax, x_vals, y_prime, analysis, p_prime: sp.Poly, x_sym: sp.Symbol):
    ax.set_facecolor("#161b2e")
    ax.grid(True, linestyle=":", alpha=0.3, color="#555555")
    for spine in ax.spines.values():
        spine.set_color("#444455")

    ax.axhline(0, color="#888888", linewidth=1.0, linestyle="-", alpha=0.55)

    deriv_color = "#ce93d8"
    ax.plot(x_vals, y_prime, color=deriv_color, linewidth=2.0, label=r"$p'(x)$")

    # Mark the zeros of the derivative (exactly the turning points of p)
    for tp in analysis.turning_points:
        ax.scatter([tp.x], [0.0], s=85, c="#ffab40", edgecolors="white", linewidths=1.1,
                   marker="D", zorder=5)
        ax.axvline(tp.x, color="#ffab40", linestyle=":", linewidth=1.0, alpha=0.4)

    ax.set_title(r"Derivative $p'(x)$ — zeros mark turning points of $p(x)$", fontsize=11, pad=6)
    ax.set_xlabel(r"$x$", fontsize=10)
    ax.set_ylabel(r"$p'(x)$", fontsize=10)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.8)


# =============================================================================
# Complex roots plane
# =============================================================================

def _plot_complex_roots_plane(ax, analysis: PolynomialAnalysis):
    ax.set_facecolor("#161b2e")
    ax.grid(True, linestyle=":", alpha=0.3, color="#555555")
    for spine in ax.spines.values():
        spine.set_color("#444455")

    ax.axhline(0, color="#777777", linewidth=1.0, linestyle="-", alpha=0.6)
    ax.axvline(0, color="#777777", linewidth=1.0, linestyle="-", alpha=0.6)

    real_roots = get_real_roots(analysis)
    complex_roots = get_complex_roots(analysis)

    # Real roots (on the real axis) — larger and distinct
    if real_roots:
        reals_x = [r.real_value for r in real_roots]
        reals_y = [0.0] * len(reals_x)
        sizes = [160 + 70 * (r.multiplicity - 1) for r in real_roots]
        ax.scatter(
            reals_x, reals_y,
            s=sizes,
            c="#ff5252",
            edgecolors="white",
            linewidths=1.4,
            marker="o",
            label="Real roots",
            zorder=4,
        )

    # Non-real complex roots (purple, smaller)
    if complex_roots:
        cx = [r.value.real for r in complex_roots]
        cy = [r.value.imag for r in complex_roots]
        ax.scatter(
            cx, cy,
            s=95,
            c="#7c4dff",
            edgecolors="#e1bee7",
            linewidths=0.9,
            marker="o",
            label="Complex (non-real)",
            zorder=4,
        )

    # Make axes equal and give a little padding
    all_re = [r.value.real for r in analysis.roots] or [0.0]
    all_im = [r.value.imag for r in analysis.roots] or [0.0]
    max_abs_re = max(abs(min(all_re)), abs(max(all_re)), 1.0) * 1.25
    max_abs_im = max(abs(min(all_im)), abs(max(all_im)), 0.8) * 1.35

    ax.set_xlim(-max_abs_re, max_abs_re)
    ax.set_ylim(-max_abs_im, max_abs_im)
    ax.set_aspect("equal", adjustable="box")

    ax.set_title("Roots in the Complex Plane  (ℂ)", fontsize=11, pad=6)
    ax.set_xlabel("Re", fontsize=10)
    ax.set_ylabel("Im", fontsize=10)

    # Helpful note for students
    if complex_roots:
        ax.text(
            0.02, 0.98,
            "Non-real roots appear\nin conjugate pairs",
            transform=ax.transAxes,
            fontsize=8,
            color="#c5b3ff",
            va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#211a36", edgecolor="#5c4a8a", alpha=0.85),
        )

    ax.legend(loc="lower right", fontsize=8, framealpha=0.85)


# =============================================================================
# Utility functions
# =============================================================================

def _choose_x_window(
    analysis: PolynomialAnalysis,
    poly: sp.Poly,
    x_sym: sp.Symbol,
    margin_factor: float = 0.65,
) -> Tuple[float, float]:
    """
    Choose a sensible plotting interval that includes all real roots and
    turning points, with extra margin so end behavior arrows are visible.

    Special cases (no real features): fall back to a window that still shows
    the overall shape (degree-dependent).
    """
    interesting_x: List[float] = []

    for r in analysis.roots:
        if r.is_real:
            interesting_x.append(r.real_value)

    for tp in analysis.turning_points:
        interesting_x.append(tp.x)

    if not interesting_x:
        # No real roots or turning points — e.g. x^2 + 1, x^4 + 3, etc.
        # Choose a reasonable default that grows gently with degree
        base = 2.8 + 0.6 * min(analysis.degree, 6)
        return -base, base

    x_min = min(interesting_x)
    x_max = max(interesting_x)

    if x_min == x_max:
        # Single interesting point (e.g. double root at 0)
        pad = 2.5 + 0.4 * analysis.degree
        return x_min - pad, x_max + pad

    span = x_max - x_min
    pad = max(1.2, margin_factor * span) + 0.3 * analysis.degree
    return x_min - pad, x_max + pad


def _evaluate_poly_numpy(poly: sp.Poly, x_sym: sp.Symbol, x_vals: np.ndarray) -> np.ndarray:
    """
    Fast numeric evaluation using lambdify (preferred over slow subs loop).
    Falls back safely if lambdify has issues with the domain.
    """
    try:
        f = sp.lambdify(x_sym, poly.as_expr(), modules=["numpy"])
        y = np.asarray(f(x_vals), dtype=float)
        return y
    except Exception:
        # Slow but robust fallback
        y = np.empty_like(x_vals, dtype=float)
        for i, xv in enumerate(x_vals):
            y[i] = float(poly.eval(xv))
        return y
