import React from 'react';
import { ChevronDown, ListChecks } from 'lucide-react';
import type { StepByStepSolution, SolverStep } from '../utils/polynomial';
import { formatNumber } from '../utils/polynomial';

interface Props {
  solution: StepByStepSolution | null;
  onCompute: () => void;
  isComputing?: boolean;
}

export const StepByStep: React.FC<Props> = ({ solution, onCompute, isComputing }) => {
  const [isOpen, setIsOpen] = React.useState(true);

  const renderStep = (step: SolverStep, index: number) => {
    return (
      <div key={index} className="step-card">
        <div className="step-title">
          <ListChecks size={15} className="text-[var(--primary)]" />
          {step.title}
        </div>
        <div className="step-explain">{step.explanation}</div>

        {/* Synthetic Division — elegant table */}
        {step.synthetic && (
          <div className="my-4 overflow-x-auto">
            <table className="synthetic-table">
              <tbody>
                <tr>
                  <th className="w-12">{step.synthetic.rootStr}</th>
                  {step.synthetic.coeffsRow.map((c, i) => (
                    <td key={i}>{formatNumber(c)}</td>
                  ))}
                </tr>
                <tr>
                  <th></th>
                  <td></td>
                  {step.synthetic.productsRow.slice(1).map((p, i) => (
                    <td key={i}>{formatNumber(p)}</td>
                  ))}
                </tr>
                <tr>
                  <th></th>
                  {step.synthetic.bottomRow.map((b, i) => (
                    <td
                      key={i}
                      className={i === step.synthetic!.bottomRow.length - 1 ? 'font-semibold bg-[#EEF2FF]' : ''}
                    >
                      {formatNumber(b)}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
            <div className="text-[12px] text-[var(--text-muted)] mt-1">
              Quotient = <span className="mono text-[var(--text)]">{step.synthetic.quotientStr}</span>
              &nbsp;&nbsp;·&nbsp;&nbsp; Remainder = {formatNumber(step.synthetic.remainder)}
            </div>
          </div>
        )}

        {/* Completing the Square — calm, readable steps */}
        {step.completeSquare && step.completeSquare.length > 0 && (
          <div className="my-4">
            <div className="text-[11px] font-medium uppercase tracking-widest text-[var(--text-muted)] mb-1.5 pl-1">
              Completing the square
            </div>
            <div className="complete-square">
              {step.completeSquare.map((line, li) => (
                <div key={li}>{line}</div>
              ))}
            </div>
          </div>
        )}

        {/* Roots contributed by this step */}
        {step.rootsFound && step.rootsFound.length > 0 && (
          <div className="mt-2 text-sm">
            <span className="text-[var(--text-muted)]">Root{step.rootsFound.length > 1 ? 's' : ''}:</span>{' '}
            {step.rootsFound.map((r, ri) => (
              <span key={ri} className="mono font-semibold ml-2 text-[var(--root)]">
                {formatNumber(r.value)}{r.multiplicity > 1 ? `×${r.multiplicity}` : ''}
              </span>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="card">
      {/* Header */}
      <div className="px-6 pt-5 pb-4 border-b border-[var(--border)] flex flex-col sm:flex-row sm:items-center justify-between gap-y-3">
        <div>
          <div className="section-label tracking-[0.065em]">DETAILED ALGEBRAIC SOLUTION</div>
          <div className="text-lg font-semibold text-[var(--text)] tracking-tight mt-0.5">
            Factor &amp; Solve Step by Step
          </div>
          <div className="text-sm text-[var(--text-muted)] mt-0.5">
            Rational Root Theorem • Synthetic Division • Completing the Square
          </div>
          <div className="text-[10px] text-[var(--primary)] font-medium tracking-wide mt-0.5">
            Pure classical math — no AI, no cloud, runs 100% locally
          </div>
        </div>

        <button
          onClick={onCompute}
          disabled={isComputing}
          className="btn btn-primary text-sm px-6 py-2.5 self-start sm:self-auto"
        >
          {isComputing ? 'Working…' : 'Factor & Solve with Steps'}
        </button>
      </div>

      {/* Content */}
      {!solution && (
        <div className="px-6 py-8 text-[15px] text-[var(--text-muted)] max-w-prose space-y-3">
          <p>
            Click the button to generate a complete, hand-work style walkthrough. You will see the exact candidates from the Rational Root Theorem, every synthetic division table, and (when applicable) a full completing-the-square derivation.
          </p>
          <p className="text-xs font-medium text-[var(--primary)]">
            Pure classical mathematics — 100% deterministic code running locally in your browser.
            No AI, no LLMs, no external services. Every step follows standard textbook algebra.
          </p>
        </div>
      )}

      {solution && (
        <div className="px-6 pt-5 pb-6 space-y-4">
          {/* Prominent factored result */}
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 pb-1">
            <div className="font-semibold text-[var(--text)] tracking-tight">Factored form</div>
            <div className="mono text-[15px] font-medium px-3 py-1 bg-[#EEF2FF] text-[var(--primary)] rounded-lg border border-[#C7D2FE]">
              {solution.factoredForm}
            </div>
            {!solution.hasExactSolution && (
              <span className="text-xs px-2.5 py-px rounded bg-amber-100 text-amber-800 self-start">Some roots numeric</span>
            )}
          </div>
          <div className="text-[10px] text-[var(--text-muted)] -mt-1">
            All steps generated by ordinary deterministic JavaScript (no AI).
          </div>

          <div className="flex justify-end">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="btn btn-ghost text-xs flex items-center gap-1 py-1 px-3"
            >
              {isOpen ? 'Collapse steps' : 'Expand steps'}
              <ChevronDown size={15} className={`transition ${isOpen ? 'rotate-180' : ''}`} />
            </button>
          </div>

          {isOpen && (
            <div className="pt-1">
              {solution.steps.length === 0 ? (
                <div className="text-sm text-[var(--text-muted)]">No further algebraic steps required.</div>
              ) : (
                solution.steps.map((step, idx) => renderStep(step, idx))
              )}

              <div className="text-[11px] text-[var(--text-muted)] pt-5 border-t border-[var(--border)] mt-4">
                All steps use only classical pencil-and-paper algebra executed locally with ordinary JavaScript (Rational Root Theorem + synthetic division + completing the square). 
                No AI, no LLMs, and no external services are used at any point.
                {solution.hasExactSolution ? ' This factorization is fully exact.' : ''}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
