import { useState } from "react";

// ── SE BRAND DESIGN SYSTEM (shared across all 4 exhibits) ──
const SE = {
  dark: '#0A2F24',
  green: '#3DCD58',
  red: '#FF0050',
  amber: '#FFCE00',
  cyan: '#24F0FF',
  blue: '#2040FF',
  bg: '#FFFFFF',
  card: '#FAFAF8',
  border: '#E5E3DE',
  textPrimary: '#0A2F24',
  textSecondary: '#6B6860',
  textMuted: '#A8A49C',
};

// Channel → SE brand color
const CH = {
  BI:      { color: SE.blue,  label: 'Business Interruption' },
  Carbon:  { color: SE.green, label: 'Carbon Costs' },
  Damage:  { color: SE.red,   label: 'Physical Damage' },
  Cooling: { color: SE.amber, label: 'Cooling Stress' },
  HPL:     { color: SE.cyan,  label: 'Heat Productivity' },
};

const regions = [
  {
    name: 'United States', total: 108, pct: '27.6%',
    channels: [
      { key: 'BI', val: 48 }, { key: 'Cooling', val: 27 },
      { key: 'Damage', val: 20 }, { key: 'Carbon', val: 12 }, { key: 'HPL', val: 1 },
    ]
  },
  {
    name: 'China', total: 111, pct: '55.8%',
    channels: [
      { key: 'Carbon', val: 36 }, { key: 'Damage', val: 33 },
      { key: 'BI', val: 31 }, { key: 'Cooling', val: 10 }, { key: 'HPL', val: 1 },
    ]
  },
  {
    name: 'Europe', total: 107, pct: '53.1%',
    channels: [
      { key: 'Carbon', val: 45 }, { key: 'BI', val: 26 },
      { key: 'Cooling', val: 23 }, { key: 'Damage', val: 12 }, { key: 'HPL', val: 1 },
    ]
  },
  {
    name: 'APMEA', total: 62, pct: '28.2%',
    channels: [
      { key: 'Damage', val: 18 }, { key: 'BI', val: 16 },
      { key: 'Carbon', val: 15 }, { key: 'Cooling', val: 12 }, { key: 'HPL', val: 1 },
    ]
  },
];

export default function Treemap() {
  const [hover, setHover] = useState(null);
  const W = 960, H = 650;
  const pad = 24, gap = 16;
  const rows = [[regions[0], regions[1]], [regions[2], regions[3]]];
  const drawW = W - 2 * pad - gap;
  const drawH = H - 2 * pad - gap - 32;
  const rowH = (drawH - gap) / 2;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', background: SE.bg, fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif" }}>
      <defs>
        <filter id="shadow" x="-2%" y="-1%" width="104%" height="106%">
          <feDropShadow dx="0" dy="1.5" stdDeviation="4" floodColor="#000" floodOpacity="0.05"/>
        </filter>
      </defs>

      {rows.map((row, ri) => {
        const rowTotal = row.reduce((s, r) => s + r.total, 0);
        const y0 = pad + ri * (rowH + gap);
        let x0 = pad;

        return row.map((reg, ci) => {
          const rw = (reg.total / rowTotal) * drawW;
          const rx = x0;
          x0 += rw + gap;
          const hdrH = 44;
          const iX = rx + 10, iY = y0 + hdrH, iW = rw - 20, iH = rowH - hdrH - 10;
          const chSum = reg.channels.reduce((s, c) => s + c.val, 0);
          let cx = iX;

          return (
            <g key={`${ri}${ci}`}>
              <rect x={rx} y={y0} width={rw} height={rowH}
                    fill={SE.card} stroke={SE.border} strokeWidth={1} rx={8}
                    filter="url(#shadow)" />
              <text x={rx + 16} y={y0 + 20} fill={SE.textPrimary} fontSize={14} fontWeight="700">
                {reg.name}
              </text>
              <text x={rx + 16} y={y0 + 36} fill={SE.textSecondary} fontSize={11}>
                ${reg.total}B ClimVaR · {reg.pct} intensity
              </text>
              <line x1={rx + 12} y1={y0 + hdrH - 2} x2={rx + rw - 12} y2={y0 + hdrH - 2}
                    stroke={SE.border} strokeWidth={0.5} />

              {reg.channels.filter(c => c.val > 0).map((ch, ki) => {
                const tw = iW * ch.val / chSum;
                const tX = cx;
                cx += tw;
                const isH = hover === `${reg.name}-${ch.key}`;
                const c = CH[ch.key];

                return (
                  <g key={ki}
                     onMouseEnter={() => setHover(`${reg.name}-${ch.key}`)}
                     onMouseLeave={() => setHover(null)}
                     style={{ cursor: 'pointer' }}>
                    <rect x={tX + 1.5} y={iY} width={tw - 3} height={iH}
                          fill={c.color} opacity={isH ? 0.82 : 0.65} rx={4} />
                    {tw > 55 && (
                      <text x={tX + tw/2} y={iY + iH/2 - 6} textAnchor="middle"
                            fill="white" fontSize={11} fontWeight="600">{ch.key}</text>
                    )}
                    {tw > 40 && (
                      <text x={tX + tw/2} y={iY + iH/2 + 12} textAnchor="middle"
                            fill="rgba(255,255,255,0.8)" fontSize={10}>${ch.val}B</text>
                    )}
                  </g>
                );
              })}
              {(() => { cx = iX; return null; })()}
            </g>
          );
        });
      })}

      {/* Legend */}
      <g transform={`translate(${W/2 - 210}, ${H - 50})`}>
        {Object.entries(CH).filter(([k]) => k !== 'HPL').map(([key, ch], i) => (
          <g key={key} transform={`translate(${i * 108}, 0)`}>
            <rect width={13} height={13} fill={ch.color} rx={3} opacity={0.65} />
            <text x={18} y={10.5} fill={SE.textSecondary} fontSize={10.5}>{ch.label}</text>
          </g>
        ))}
      </g>

      {/* Footer */}
      <line x1={120} y1={H - 28} x2={W - 120} y2={H - 28}
            stroke={SE.border} strokeWidth={0.5} />
      <text x={W/2} y={H - 10} textAnchor="middle" fill={SE.textMuted} fontSize={9}>
        Area proportional to ClimVaR in US$B · BAU/MEAN · Installed base
      </text>

      {hover && (() => {
        const [rn, cn] = hover.split('-');
        const reg = regions.find(r => r.name === rn);
        const ch = reg?.channels.find(c => c.key === cn);
        if (!ch) return null;
        return (
          <g transform={`translate(${W - 240}, ${H - 98})`}>
            <rect width={224} height={46} fill={SE.dark} rx={8} opacity={0.92} />
            <text x={112} y={18} textAnchor="middle" fill="white" fontSize={11}>{rn} · {CH[ch.key].label}</text>
            <text x={112} y={36} textAnchor="middle" fill={SE.green} fontSize={12} fontWeight="700">
              ${ch.val}B — {Math.round(ch.val / reg.total * 100)}% of regional
            </text>
          </g>
        );
      })()}
    </svg>
  );
}
