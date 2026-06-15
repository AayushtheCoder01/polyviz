# polynomial-explorer

A clean, beautiful, and rigorously educational Python tool for deeply understanding **polynomials**.

Focus areas:
- Roots (real and complex) **with multiplicity**
- **End behavior** (degree + leading coefficient) — explained in text *and* shown visually with arrows
- **Turning points** found by solving the derivative, classified with the second derivative test
- High-quality matplotlib visualizations that make the algebra visible

Built with `numpy`, `sympy`, and `matplotlib`. Designed to be used both from the command line and inside Jupyter notebooks.

---

## Mathematical Concepts the Tool Teaches

| Concept                    | What the tool shows                                                                 |
|----------------------------|-------------------------------------------------------------------------------------|
| **Degree & Leading Term**  | Determines end behavior. The tool prints a clear description and draws arrows on the plot. |
| **Roots + Multiplicity**   | Real roots are marked on the graph with size indicating multiplicity. A complex-plane subplot shows all roots (real roots lie on the real axis). |
| **Even vs Odd Multiplicity** | Even multiplicity → graph touches and turns back. Odd multiplicity → graph crosses (possibly flat). |
| **Turning Points**         | Found by solving `p'(x) = 0`. The second derivative test classifies local max / min / inflection. A dedicated subplot of `p'(x)` makes the relationship obvious. |
| **End Behavior**           | Four canonical cases (even/odd degree × positive/negative leading coefficient). Visual arrows + text. |
| **Complex Conjugate Pairs**| For real coefficients, non-real roots appear in conjugate pairs — visible in the complex plane plot. |

---

## Project Structure

```
polynomial-explorer/
├── .venv/                     # virtual environment (created by you)
├── src/
│   └── polynomial_explorer/
│       ├── __init__.py        # public API: explore(), analyze_polynomial(), ...
│       ├── parser.py          # robust string & list → sympy.Poly
│       ├── analysis.py        # pure math: roots, derivative, end behavior, summary
│       ├── visualization.py   # stunning educational matplotlib figures
│       ├── explorer.py        # high-level one-function API
│       └── __main__.py        # CLI entry point
├── examples/
│   └── demo.py                # curated set of educational examples
├── main.py                    # run without installing: `python main.py "..." `
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

Logic is cleanly separated:
- `analysis.py` — no plotting, only mathematics (easy to test or reuse)
- `visualization.py` — only plotting (receives analysis results)

---

## Quick Start

### 1. Create virtual environment & install

```powershell
# Windows (PowerShell)
cd C:\Users\PC\Desktop\polynomial-explorer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# (Optional) install in editable mode so the CLI command works
pip install -e .
```

### 2. Run from the command line

```powershell
# Using the convenience launcher (no install needed)
python main.py "2x^3 - 3x^2 + 5"

# Or after `pip install -e .`
poly-explore "x^2 - 1"

# Built-in educational examples (highly recommended first run)
python main.py --examples
# or
python -m polynomial_explorer --examples

# Interactive mode
python main.py --interactive
```

### 3. Use from Python / Jupyter

```python
from polynomial_explorer import explore

# String input (very flexible)
analysis = explore("2x^3 - 3x^2 + 5")

# List of coefficients (highest degree first)
explore([1, -6, 11, -6])          # (x-1)(x-2)(x-3)

# Just get the math without the plot
analysis = explore("x^4 - 5x^2 + 4", show_plot=False)
print(analysis.degree)
print(analysis.end_behavior)
for r in analysis.roots:
    print(r.value, "mult =", r.multiplicity)
```

---

## Input Formats Supported

**String** (student-friendly):
- `"2x^3 - 3x^2 + 5"`
- `"x^2-x-6"`
- `"(x-2)^2*(x-5)"`
- `"-0.5x^4 + x - 1"`
- `"x"` , `"5"`, `"-x^3"`

**Coefficient list** (highest power first):
- `[2, -3, 0, 5]` → `2x^3 - 3x^2 + 5`
- `[1, 0, -2]` → `x^2 - 2`

The parser uses SymPy's excellent transformations so implicit multiplication and `^` both work.

---

## Example Output (Text Summary)

```
======================================================================
                        POLYNOMIAL ANALYSIS
======================================================================

p(x) = x^3 - 6*x^2 + 11*x - 6
Degree: 3
Leading coefficient: 1

END BEHAVIOR
--------------------
Odd degree with positive leading coefficient → from -∞ to +∞.
    As x → -∞, p(x) → -∞    and    As x → +∞, p(x) → +∞

ROOTS (with multiplicity)
--------------------
  Root                     Multiplicity       Type
  ------------------------------------------------
  1                             1            Real
  2                             1            Real
  3                             1            Real

TURNING POINTS (critical points)
--------------------
             x           p(x)  Kind                   p''(x) sign
  ------------------------------------------------------------------
      1.57735      -1.38481  local min                 negative
      3.42265       1.38481  local max                 positive

======================================================================
```

---

## The Visualization (what makes it special)

The generated figure contains three coordinated views:

1. **Main plot** — smooth curve of `p(x)`
   - Large, distinct markers for real roots (size grows with multiplicity)
   - Orange diamonds + dashed projection lines for every turning point
   - Green arrows + ∞ labels at both ends showing end behavior
   - Info box with degree + leading coefficient

2. **Derivative subplot** — `p'(x)`
   - Clearly shows that turning points of `p` are exactly the zeros of `p'`
   - Turning points are marked on the derivative plot as well

3. **Complex plane subplot**
   - All roots plotted in ℂ
   - Real roots appear on the horizontal axis (larger markers)
   - Non-real roots appear in symmetric conjugate pairs

This layout makes the following ideas **visually obvious**:
- Where the graph crosses or touches the x-axis
- Why a double root creates a flat "bounce"
- How the derivative tells you the location of hills and valleys
- That complex roots don't appear on the real graph but still exist in pairs

---

## Tips for Learning & Teaching

- Start with `python main.py --examples`
- Try polynomials with repeated roots: `(x-1)^2`, `(x+2)^3`
- Compare even vs odd degree with the same leading sign
- Look at the complex plane for `x^2 + 1`, `x^2 + 2x + 5`
- Use the derivative subplot to explain the second derivative test
- In Jupyter, call `explore(...)` in one cell, then tweak the returned `fig` and `axes` in the next cell

---

## Development / Extending

```powershell
# After activating .venv
pip install -e .

# Run the full demo
python examples/demo.py

# Run a single polynomial from the package
python -m polynomial_explorer "x^5 - x"
```

The public API is intentionally small and well-documented:
- `explore(...)` — the 90% use case
- `analyze_polynomial(poly)` — pure math result (great for exercises or autograders)
- `plot_polynomial(poly, analysis=...)` — full control over the figure

All core mathematics lives in `analysis.py` and uses SymPy for exact results wherever possible.

---

## License & Credits

Created as an educational project (2026). Feel free to use, modify, and share for teaching and learning.

Happy exploring!
```

Now update todo.