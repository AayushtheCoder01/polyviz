import React from 'react';

interface Example {
  label: string;
  expr: string;
}

interface Props {
  onSelect: (expr: string) => void;
}

const EXAMPLES: Example[] = [
  { label: '(x−1)(x−2)(x−3)', expr: 'x^3 - 6x^2 + 11x - 6' },
  { label: '2x^3 − 5x^2 + 1', expr: '2x^3 - 5x^2 + 1' },
  { label: 'x^2 − 1', expr: 'x^2 - 1' },
  { label: '(x−1)^2', expr: 'x^2 - 2x + 1' },
  { label: 'x^4 − 5x^2 + 4', expr: 'x^4 - 5x^2 + 4' },
  { label: 'x^3 − x', expr: 'x^3 - x' },
  { label: '(x+2)^3', expr: 'x^3 + 6x^2 + 12x + 8' },
];

export const QuickExamples: React.FC<Props> = ({ onSelect }) => {
  return (
    <div>
      <div className="label mb-2">Quick examples</div>
      <div className="flex flex-wrap gap-2">
        {EXAMPLES.map((ex, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(ex.expr)}
            className="example-chip hover-lift"
            title={`Load ${ex.expr}`}
          >
            {ex.label}
          </button>
        ))}
      </div>
    </div>
  );
};
