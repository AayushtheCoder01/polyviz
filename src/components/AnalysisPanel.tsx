import React from 'react';
import type { PolynomialAnalysis, RealRoot, TurningPoint } from '../utils/polynomial';
import { formatNumber } from '../utils/polynomial';

interface Props {
  analysis: PolynomialAnalysis;
  onHighlightRoot?: (value: number | null) => void;
  onHighlightTurning?: (x: number | null) => void;
}

export const AnalysisPanel: React.FC<Props> = ({
  analysis,
  onHighlightRoot,
  onHighlightTurning,
}) => {
  const { degree, leadingCoeff, endBehavior, roots, turningPoints } = analysis;

  return (
    <div className="card p-6 space-y-7 h-full flex flex-col">
      <div>
        <div className="section-label">ANALYSIS</div>
        <div className="mt-1 text-xl font-semibold tracking-tighter text-[var(--text)]">
          Degree {degree} &nbsp;·&nbsp; Leading coeff {formatNumber(leadingCoeff)}
        </div>
      </div>

      {/* End Behavior */}
      <div>
        <div className="font-semibold text-[var(--text)] mb-2 tracking-tight">End Behavior</div>
        <div className="text-sm leading-relaxed bg-[#F8FAFC] border border-[var(--border)] rounded-xl p-4">
          <div className="font-medium mb-1.5 text-[var(--text)]">{endBehavior.description}</div>
          <div className="grid grid-cols-1 gap-y-1 text-[var(--text-muted)]">
            <div>{endBehavior.left}</div>
            <div>{endBehavior.right}</div>
          </div>
        </div>
      </div>

      {/* Roots — interactive for graph connection */}
      <div className="flex-1">
        <div className="font-semibold text-[var(--text)] mb-2 flex items-center gap-2 tracking-tight">
          Real Roots
          <span className="badge root-badge">{roots.length}</span>
        </div>

        {roots.length === 0 ? (
          <div className="text-sm text-[var(--text-muted)] py-1">No real roots.</div>
        ) : (
          <div className="space-y-1">
            {roots.map((r: RealRoot, idx: number) => (
              <div
                key={idx}
                className="analysis-row root flex items-center justify-between text-sm group"
                onMouseEnter={() => onHighlightRoot?.(r.value)}
                onMouseLeave={() => onHighlightRoot?.(null)}
              >
                <div className="flex items-center gap-2">
                  <span className="mono font-semibold text-[var(--root)]">{formatNumber(r.value)}</span>
                  {r.multiplicity > 1 && (
                    <span className="text-[10px] px-1.5 py-px rounded bg-emerald-100 text-emerald-700 font-medium">
                      ×{r.multiplicity}
                    </span>
                  )}
                </div>
                <div className="text-xs text-[var(--text-muted)]">
                  {r.multiplicity % 2 === 0 ? 'touches (even)' : 'crosses (odd)'}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Turning Points — interactive */}
      <div>
        <div className="font-semibold text-[var(--text)] mb-2 flex items-center gap-2 tracking-tight">
          Turning Points
          <span className="badge turn-badge">{turningPoints.length}</span>
        </div>

        {turningPoints.length === 0 ? (
          <div className="text-sm text-[var(--text-muted)] py-1">No real turning points.</div>
        ) : (
          <div className="space-y-1">
            {turningPoints.map((tp: TurningPoint, idx: number) => (
              <div
                key={idx}
                className="analysis-row turn flex items-center justify-between text-sm"
                onMouseEnter={() => onHighlightTurning?.(tp.x)}
                onMouseLeave={() => onHighlightTurning?.(null)}
              >
                <div>
                  <span className="mono font-semibold text-[var(--turn)]">{formatNumber(tp.x)}</span>
                  <span className="mx-1.5 text-[var(--text-muted)]">→</span>
                  <span className="mono">{formatNumber(tp.y)}</span>
                </div>
                <div className="text-xs capitalize text-[var(--text-muted)]">{tp.kind}</div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-3 text-[10px] leading-snug text-[var(--text-muted)]">
          Turning points are where p′(x) = 0. Classification uses the second derivative test.
        </div>
      </div>
    </div>
  );
};
