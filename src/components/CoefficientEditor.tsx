import React from 'react';
import { Plus, Minus, RotateCcw } from 'lucide-react';
import type { Coeffs } from '../utils/polynomial';

interface Props {
  coeffs: Coeffs;
  onChange: (newCoeffs: Coeffs) => void;
}

export const CoefficientEditor: React.FC<Props> = ({ coeffs, onChange }) => {
  const display = [...coeffs];

  const update = (idx: number, raw: string) => {
    const val = parseFloat(raw);
    const next = [...display];
    next[idx] = isNaN(val) ? 0 : val;
    onChange(next);
  };

  const addHigher = () => onChange([0, ...display]);

  const removeHighest = () => {
    if (display.length <= 1) return;
    onChange(display.slice(1));
  };

  const reset = () => onChange([1, 0]);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <div className="label">Manual Coefficients</div>
          <div className="text-[10px] text-[var(--text-muted)] -mt-0.5">
            Highest power on the left (live updates)
          </div>
        </div>

        <div className="flex gap-1.5">
          <button
            onClick={addHigher}
            className="btn btn-secondary text-xs px-2.5 py-1.5"
            title="Add higher-degree term"
          >
            <Plus size={14} /> Higher
          </button>
          <button
            onClick={removeHighest}
            disabled={display.length <= 1}
            className="btn btn-secondary text-xs px-2.5 py-1.5 disabled:opacity-50"
            title="Remove highest power"
          >
            <Minus size={14} />
          </button>
          <button
            onClick={reset}
            className="btn btn-ghost text-xs px-2.5 py-1.5"
            title="Reset to x"
          >
            <RotateCcw size={14} />
          </button>
        </div>
      </div>

      <div className="flex flex-wrap gap-2.5 p-4 rounded-2xl border border-[var(--border)] bg-[var(--surface-2)]">
        {display.map((c, idx) => {
          const power = display.length - 1 - idx;
          const label = power === 0 ? 'const' : power === 1 ? 'x' : `x^${power}`;
          return (
            <div key={idx} className="coeff-cell">
              <input
                type="text"
                inputMode="decimal"
                value={c}
                onChange={(e) => update(idx, e.target.value)}
                className="input input-mono coeff-input shadow-sm"
              />
              <div className="text-[10px] mt-1 text-[var(--text-muted)] mono tracking-tight">
                {label}
              </div>
            </div>
          );
        })}

        {display.length === 0 && (
          <div className="text-xs text-[var(--text-muted)] py-2">Add a higher power to begin.</div>
        )}
      </div>
    </div>
  );
};
