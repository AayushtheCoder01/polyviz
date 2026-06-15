import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import type { Coeffs, RealRoot, TurningPoint } from '../utils/polynomial';
import { derivative, samplePolynomial, polyToString } from '../utils/polynomial';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend, Title);

interface Props {
  coeffs: Coeffs;
  showDerivative: boolean;
  onToggleDerivative: (v: boolean) => void;
  viewWindow?: { min: number; max: number };
  roots: RealRoot[];
  turningPoints: TurningPoint[];
  // For delightful cross-component micro-interactions
  highlightedRoot?: number | null;
  highlightedTurningX?: number | null;
}

export const InteractiveGraph: React.FC<Props> = ({
  coeffs,
  showDerivative,
  onToggleDerivative,
  viewWindow,
  roots,
  turningPoints,
  highlightedRoot = null,
  highlightedTurningX = null,
}) => {
  const { min: xMin, max: xMax } = React.useMemo(() => {
    if (viewWindow) return viewWindow;
    return { min: -6.8, max: 6.8 };
  }, [viewWindow]);

  const mainPoints = React.useMemo(
    () => samplePolynomial(coeffs, xMin, xMax, 360),
    [coeffs, xMin, xMax]
  );

  const derivCoeffs = React.useMemo(() => derivative(coeffs), [coeffs]);
  const derivPoints = React.useMemo(() => {
    if (!showDerivative) return [];
    return samplePolynomial(derivCoeffs, xMin, xMax, 320);
  }, [showDerivative, derivCoeffs, xMin, xMax]);

  // Premium color mapping
  const INDIGO = '#4338CA';
  const EMERALD = '#10B981';
  const AMBER = '#F59E0B';
  const SLATE_MUTED = '#64748B';

  const datasets: any[] = [
    {
      label: `p(x) = ${polyToString(coeffs)}`,
      data: mainPoints,
      borderColor: INDIGO,
      borderWidth: 2.75,
      pointRadius: 0,
      tension: 0.28,
      order: 3,
    },
  ];

  if (showDerivative) {
    datasets.push({
      label: `p′(x)`,
      data: derivPoints,
      borderColor: SLATE_MUTED,
      borderWidth: 2,
      borderDash: [4, 3],
      pointRadius: 0,
      tension: 0.22,
      order: 4,
    });
  }

  // Roots — emerald, dynamic size on highlight
  if (roots.length > 0) {
    const rootData = roots.map((r) => ({ x: r.value, y: 0 }));
    const pointRadii = roots.map((r) => {
      const base = 7.5 + Math.min((r.multiplicity - 1) * 2.2, 6);
      const isHighlighted = highlightedRoot != null && Math.abs(r.value - highlightedRoot) < 1e-6;
      return isHighlighted ? base * 1.55 : base;
    });

    datasets.push({
      label: 'Real roots',
      data: rootData,
      borderColor: EMERALD,
      backgroundColor: EMERALD,
      pointRadius: pointRadii,
      pointHoverRadius: 11,
      pointBorderWidth: 2.5,
      pointBorderColor: '#fff',
      showLine: false,
      order: 2,
    });
  }

  // Turning points — amber
  if (turningPoints.length > 0) {
    const turnData = turningPoints.map((t) => ({ x: t.x, y: t.y }));
    const pointRadii = turningPoints.map((t) => {
      const isHighlighted = highlightedTurningX != null && Math.abs(t.x - highlightedTurningX) < 1e-6;
      return isHighlighted ? 9.5 : 6.5;
    });

    datasets.push({
      label: 'Turning points',
      data: turnData,
      borderColor: AMBER,
      backgroundColor: AMBER,
      pointRadius: pointRadii,
      pointHoverRadius: 9.5,
      pointStyle: 'rectRot',
      pointBorderWidth: 2,
      pointBorderColor: '#fff',
      showLine: false,
      order: 1,
    });
  }

  const options = React.useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'linear' as const,
          min: xMin,
          max: xMax,
          grid: { color: '#E2E8F0', lineWidth: 0.5 },
          ticks: { color: '#64748B', font: { size: 11, weight: 500 } },
          title: { display: true, text: 'x', color: '#475569', font: { size: 12, weight: 600 } },
        },
        y: {
          grid: { color: '#E2E8F0', lineWidth: 0.5 },
          ticks: { color: '#64748B', font: { size: 11, weight: 500 } },
          title: { display: true, text: 'y', color: '#475569', font: { size: 12, weight: 600 } },
        },
      },
      plugins: {
        legend: {
          position: 'top' as const,
          align: 'end' as const,
          labels: {
            boxWidth: 13,
            padding: 16,
            font: { size: 12, weight: 500 },
            color: '#475569',
            usePointStyle: true,
          },
        },
        tooltip: {
          displayColors: false,
          backgroundColor: '#0F172A',
          titleFont: { size: 11 },
          bodyFont: { size: 12, weight: 500 },
          callbacks: {
            label: (ctx: any) => {
              const x = Number(ctx.raw.x ?? ctx.parsed.x).toFixed(4);
              const y = Number(ctx.raw.y ?? ctx.parsed.y).toFixed(4);
              return `(${x}, ${y})`;
            },
          },
        },
      },
      elements: {
        line: { tension: 0.25 },
        point: { hitRadius: 14, hoverBorderWidth: 3 },
      },
      animation: {
        duration: 280,
        easing: 'easeOutQuart' as const,
      },
    }),
    [xMin, xMax]
  );

  const hasInterestingPoints = roots.length > 0 || turningPoints.length > 0;

  return (
    <div className="card overflow-hidden h-full flex flex-col">
      <div className="flex items-center justify-between px-6 pt-5 pb-3 border-b border-[var(--border)]">
        <div>
          <div className="section-label tracking-[0.06em]">VISUALIZATION</div>
          <div className="text-[15px] font-semibold text-[var(--text)] mt-0.5 tracking-tight">
            {polyToString(coeffs)}
          </div>
        </div>

        <label className="flex items-center gap-2 text-sm cursor-pointer select-none text-[var(--text-muted)] hover:text-[var(--text)] transition-colors">
          <input
            type="checkbox"
            checked={showDerivative}
            onChange={(e) => onToggleDerivative(e.target.checked)}
            className="w-4 h-4 accent-[var(--primary)] rounded"
          />
          <span className="font-medium">Show derivative p′(x)</span>
        </label>
      </div>

      <div className="graph-container flex-1" style={{ minHeight: 420 }}>
        <Line data={{ datasets }} options={options} />
      </div>

      <div className="px-6 py-3.5 text-[11px] text-[var(--text-muted)] border-t border-[var(--border)] bg-[#FAFBFC] flex flex-wrap gap-x-6 gap-y-1 items-center">
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-2 h-2 rounded-full" style={{ background: '#10B981' }} /> 
          Roots (size = multiplicity)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-[9px] h-[9px] rotate-45" style={{ background: '#F59E0B' }} /> 
          Turning points
        </span>
        {showDerivative && <span>Dashed = p′(x)</span>}
        {!hasInterestingPoints && (
          <span className="text-[#B45309]">No real roots or turning points in current view.</span>
        )}
      </div>
    </div>
  );
};
