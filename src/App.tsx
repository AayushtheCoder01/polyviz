import React from 'react';
import { PolynomialInput } from './components/PolynomialInput';
import { QuickExamples } from './components/QuickExamples';
import { CoefficientEditor } from './components/CoefficientEditor';
import { InteractiveGraph } from './components/InteractiveGraph';
import { AnalysisPanel } from './components/AnalysisPanel';
import { StepByStep } from './components/StepByStep';

import type { Coeffs } from './utils/polynomial';
import {
  analyze,
  parsePolynomial,
  normalize,
  type PolynomialAnalysis,
  type StepByStepSolution,
  factorAndSolveWithSteps,
  suggestViewWindow,
  polyToString,
} from './utils/polynomial';

function App() {
  // Single source of truth
  const [coeffs, setCoeffs] = React.useState<Coeffs>(() => normalize([1, -6, 11, -6]));
  const [showDerivative, setShowDerivative] = React.useState(false);

  // Step-by-step state
  const [solution, setSolution] = React.useState<StepByStepSolution | null>(null);
  const [isSolving, setIsSolving] = React.useState(false);

  // Cross-component micro-interactions (hover a root or turning point in analysis → highlight on graph)
  const [highlightedRoot, setHighlightedRoot] = React.useState<number | null>(null);
  const [highlightedTurningX, setHighlightedTurningX] = React.useState<number | null>(null);

  // Live derived data
  const analysis: PolynomialAnalysis = React.useMemo(() => analyze(coeffs), [coeffs]);
  const viewWindow = React.useMemo(() => suggestViewWindow(analysis), [analysis]);
  const currentExpr = polyToString(coeffs);

  // Handlers
  const handleCoeffsChange = React.useCallback((newCoeffs: Coeffs) => {
    const norm = normalize(newCoeffs);
    setCoeffs(norm);
    setSolution(null);
    setHighlightedRoot(null);
    setHighlightedTurningX(null);
  }, []);

  const handleParseExpression = React.useCallback((expr: string) => {
    const parsed = parsePolynomial(expr);
    const norm = normalize(parsed);
    setCoeffs(norm);
    setSolution(null);
    setHighlightedRoot(null);
    setHighlightedTurningX(null);
  }, []);

  const handleFactorAndSolve = React.useCallback(() => {
    setIsSolving(true);
    // Tiny delay makes the action feel deliberate and premium
    setTimeout(() => {
      const result = factorAndSolveWithSteps(coeffs);
      setSolution(result);
      setIsSolving(false);
    }, 35);
  }, [coeffs]);

  // Clear highlights when the polynomial fundamentally changes
  React.useEffect(() => {
    setHighlightedRoot(null);
    setHighlightedTurningX(null);
  }, [currentExpr]);

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      {/* Premium header */}
      <header className="border-b border-[var(--border)] bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3.5">
            <div className="w-9 h-9 rounded-2xl bg-[var(--primary)] flex items-center justify-center text-white shadow-sm">
              <span className="font-semibold tracking-[-1px] text-lg">P</span>
            </div>
            <div>
              <div className="font-semibold text-[22px] tracking-[-0.03em] text-[var(--text)]">PolyViz</div>
              <div className="text-[10px] text-[var(--text-muted)] -mt-1">Educational polynomial explorer</div>
            </div>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="text-sm text-[var(--text-muted)] hover:text-[var(--text)] transition-colors"
          >
            GitHub
          </a>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-5 sm:px-6 pb-16">
        {/* Hero / intro — spacious and confident */}
        <div className="pt-12 pb-8">
          <div className="max-w-3xl">
            <h1 className="tracking-tighter">
              See polynomials.<br />Understand them deeply.
            </h1>
            <p className="mt-4 text-lg text-[var(--text-muted)] max-w-[46ch]">
              A clean, modern tool for exploring polynomials visually and algebraically.
              Built for students and educators who want elegance and clarity.
            </p>
          </div>
        </div>

        {/* === DEFINITION AREA === */}
        <div className="mb-8">
          <div className="mb-3 flex items-baseline gap-3">
            <div className="section-label">DEFINE YOUR POLYNOMIAL</div>
            <div className="h-px flex-1 bg-[var(--border)]" />
          </div>

          <div className="card p-6 lg:p-7 space-y-6">
            {/* Expression row — prominent */}
            <PolynomialInput
              onParse={handleParseExpression}
              currentExpression={currentExpr}
            />

            {/* Examples — tasteful chips */}
            <QuickExamples onSelect={handleParseExpression} />

            {/* Manual coefficient editor — elegant, contained */}
            <div className="pt-2 border-t border-[var(--border)]">
              <CoefficientEditor coeffs={coeffs} onChange={handleCoeffsChange} />
            </div>
          </div>
        </div>

        {/* === VISUALIZATION + ANALYSIS (tightly connected) === */}
        <div className="mb-10">
          <div className="mb-3 flex items-baseline gap-3">
            <div className="section-label">VISUALIZE &amp; ANALYZE</div>
            <div className="h-px flex-1 bg-[var(--border)]" />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
            {/* Graph — the hero visual element */}
            <div className="xl:col-span-7">
              <InteractiveGraph
                coeffs={coeffs}
                showDerivative={showDerivative}
                onToggleDerivative={setShowDerivative}
                viewWindow={viewWindow}
                roots={analysis.roots}
                turningPoints={analysis.turningPoints}
                highlightedRoot={highlightedRoot}
                highlightedTurningX={highlightedTurningX}
              />
            </div>

            {/* Analysis — directly paired, interactive rows highlight the graph */}
            <div className="xl:col-span-5">
              <AnalysisPanel
                analysis={analysis}
                onHighlightRoot={setHighlightedRoot}
                onHighlightTurning={setHighlightedTurningX}
              />
            </div>
          </div>
        </div>

        {/* === STEP-BY-STEP — calm, beautiful, educational centerpiece === */}
        <div>
          <div className="mb-3 flex items-baseline gap-3">
            <div className="section-label">ALGEBRAIC REASONING</div>
            <div className="h-px flex-1 bg-[var(--border)]" />
          </div>

          <StepByStep
            solution={solution}
            onCompute={handleFactorAndSolve}
            isComputing={isSolving}
          />
        </div>

        {/* Subtle footer */}
        <div className="mt-12 text-center text-[11px] text-[var(--text-muted)]">
          100% classical deterministic code — no AI, no LLMs, no external services.
          <span className="mx-2">•</span>
          All mathematics implemented from scratch in TypeScript (Horner’s method • Rational Root Theorem • Synthetic division • Completing the square • Newton refinement).
        </div>
      </main>
    </div>
  );
}

export default App;
