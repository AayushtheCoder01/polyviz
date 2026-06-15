# PolyViz

Modern React + TypeScript educational polynomial visualizer and learning tool.

**Goal**: Help students deeply understand polynomials both visually and algebraically through an interactive web experience.

## Features

- **Polynomial Input**: Type expressions (`2x^3 - 5x^2 + 1`) or edit coefficients manually (highest degree first).
- **Interactive Graph** (Chart.js): Plots the curve, marks real roots (size indicates multiplicity), marks turning points, and has a toggle for the derivative curve.
- **Analysis Panel**: End behavior with explanation, list of all real roots + multiplicity, turning points with classification (local max/min via 2nd derivative test).
- **Step-by-Step Solver** (core educational feature):
  - "Factor & Solve with Steps" button
  - Rational Root Theorem candidate list
  - Full synthetic division tables for every successful factor (exactly as done by hand)
  - Completing the Square walkthrough for remaining quadratic factors
  - Honest numeric approximation + Abel–Ruffini note for higher-degree unsolvable cases
- **Everything is plain classical mathematics** — implemented from scratch in `src/utils/polynomial.ts` using only ordinary deterministic JavaScript (Horner’s method, derivative, RRT, synthetic division, completing the square, Newton refinement, etc.). No AI, no LLMs, no external CAS or APIs (unlike the original Python version which uses SymPy). All steps run locally in the browser.

## Tech Stack (as specified)

- Vite + React 19 + TypeScript
- Tailwind CSS
- Chart.js + react-chartjs-2
- lucide-react icons

## Project Structure

```
polyviz/
├── python/                    # Original Python version (moved here for preservation)
├── src/
│   ├── components/
│   │   ├── PolynomialInput.tsx
│   │   ├── PolynomialGraph.tsx
│   │   ├── AnalysisPanel.tsx
│   │   └── StepSolver.tsx
│   ├── utils/
│   │   └── polynomial.ts     # All math logic (most important file)
│   ├── App.tsx
│   └── ...
├── index.html
├── vite.config.ts
└── ...
```

## Getting Started

```powershell
# Install
npm install

# Run dev server
npm run dev

# Production build
npm run build
```

Open http://localhost:5173

## Preserved Original

The earlier Python/CLI + matplotlib version lives in the `python/` folder (with its own README). It uses numpy/sympy/matplotlib and is great for notebooks or terminal use.

## Design

Clean, spacious, serious educational UI. Excellent mobile support. Step-by-step section is collapsible and readable. All components are intentionally small and focused.

## Mathematical Notes

- Coefficients are stored **highest-degree first** (matches synthetic division and how students write polys).
- Root finding prefers exact rational roots via RRT + repeated synthetic division.
- For quadratics we demonstrate completing the square step-by-step using only deterministic string construction that mirrors manual algebra.
- Higher degree cases receive a clear explanation that no general radical solution exists (Abel–Ruffini theorem).
- **All of the above is 100% plain classical code** — ordinary hand-written JavaScript algorithms running entirely in your browser. No large language models, no AI, and no external services are involved at any point.

Happy learning!
