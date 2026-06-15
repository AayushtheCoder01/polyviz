import React from 'react';
import { Play } from 'lucide-react';

interface Props {
  onParse: (expr: string) => void;
  currentExpression: string;
}

export const PolynomialInput: React.FC<Props> = ({ onParse, currentExpression }) => {
  const [value, setValue] = React.useState('');

  const handleParse = () => {
    if (value.trim()) {
      onParse(value.trim());
      setValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleParse();
    }
  };

  return (
    <div className="space-y-2">
      <div className="label">Polynomial Expression</div>

      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. 2x^3 - 5x^2 + 1   or   x^2 - 2x + 1"
          className="input input-mono flex-1 text-[15px] shadow-sm"
          aria-label="Polynomial expression input"
        />
        <button
          onClick={handleParse}
          disabled={!value.trim()}
          className="btn btn-primary min-w-[110px] disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <Play size={16} />
          Parse
        </button>
      </div>

      <div className="text-xs text-[var(--text-muted)] flex items-center gap-2">
        <span>Current:</span>
        <span className="mono font-medium text-[var(--text)] px-2 py-px bg-[var(--surface-2)] rounded">
          {currentExpression}
        </span>
      </div>
    </div>
  );
};
