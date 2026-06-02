import { useState } from "react";

const SE = {
  dark: '#0A2F24', green: '#3DCD58', red: '#FF0050',
  amber: '#FFCE00', cyan: '#24F0FF', blue: '#2040FF',
  bg: '#FFFFFF', border: '#E5E3DE',
  textPrimary: '#0A2F24', textSecondary: '#6B6860', textMuted: '#A8A49C',
};

const scenarios = [
  { name: 'Abundance Without Boundaries', abbr: 'AWB', baseEnd: 3671, proEnd: 2536, color: SE.red },
  { name: 'Sustainable AI',               abbr: 'SAI', baseEnd: 1669, proEnd: 1134, color: SE.amber },
  { name: 'Limits to Growth',             abbr: 'LTG', baseEnd: 1008, proEnd: 669,  color: SE.blue },
];

function sig(t) { return 1 / (1 + Math.exp(-8 * (t - 0.4))); }
function traj(s, e, n = 60) {
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = i / n;
    return { yr: 2026 + t * 24, v: s + (e - s) * sig(t) };
  });
}

export default function Ribbons() {
  const [hovered, setHovered] = useState(null);
  const W = 960, H = 600;
  const pad = { l: 70, r: 200, t: 40, b: 50 };
  const pW = W - pad.l - pad.r, pH = H - pad.t - pad.b;
  const xMin = 2026, xMax = 2050, yMax = 4200;
  const xP = yr => pad.l + (yr - xMin) / (xMax - xMin) * pW;
  const yP = v => pad.t + (1 - v / yMax) * pH;

  const d = pts => pts.map((p, i) => `${i ? 'L' : 'M'}${xP(p.yr).toFixed(1)},${yP(p.v).toFixed(1)}`).join('');
  const area = (u, lo) => `${d(u)} ${[...lo].reverse().map((p, i) => `L${xP(p.yr).toFixed(1)},${yP(p.v).toFixed(1)}`).join('')} Z`;

  const yTicks = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000];
  const xTicks = [2026, 2030, 2035, 2040, 2045, 2050];

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', background: SE.bg, fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif" }}>

      {/* Grid */}
      {yTicks.map(v => (
        <g key={v}>
          <line x1={pad.l} y1={yP(v)} x2={pad.l + pW} y2={yP(v)} stroke={SE.border} strokeWidth={0.5} />
          <text x={pad.l - 10} y={yP(v) + 4} textAnchor="end" fill={SE.textMuted} fontSize={9.5}>
            {v >= 1000 ? `$${(v/1000).toFixed(1)}T` : v === 0 ? '$0' : `$${v}B`}
          </text>
        </g>
      ))}
      {xTicks.map(yr => (
        <text key={yr} x={xP(yr)} y={H - pad.b + 22} textAnchor="middle" fill={SE.textMuted} fontSize={9.5}>
          {yr}
        </text>
      ))}
      <line x1={pad.l} y1={yP(0)} x2={pad.l + pW} y2={yP(0)} stroke={SE.dark} strokeWidth={0.8} opacity={0.2} />
      <line x1={pad.l} y1={pad.t} x2={pad.l} y2={yP(0)} stroke={SE.dark} strokeWidth={0.8} opacity={0.2} />

      {/* Ribbons */}
      {scenarios.map((sc, si) => {
        const bT = traj(388, sc.baseEnd), pT = traj(238, sc.proEnd);
        const isH = hovered === si;
        return (
          <g key={si}
             onMouseEnter={() => setHovered(si)}
             onMouseLeave={() => setHovered(null)}
             style={{ cursor: 'pointer' }}>
            <path d={area(bT, pT)} fill={sc.color} opacity={isH ? 0.14 : 0.05} />
            <path d={d(bT)} fill="none" stroke={sc.color} strokeWidth={isH ? 3 : 2} />
            <path d={d(pT)} fill="none" stroke={sc.color} strokeWidth={isH ? 3 : 2}
                  strokeDasharray="7 4" opacity={0.6} />
            <circle cx={xP(2050)} cy={yP(sc.baseEnd)} r={isH ? 5 : 3.5}
                    fill={sc.color} stroke="white" strokeWidth={1.5} />
            <circle cx={xP(2050)} cy={yP(sc.proEnd)} r={isH ? 5 : 3.5}
                    fill={sc.color} stroke="white" strokeWidth={1.5} opacity={0.6} />
          </g>
        );
      })}

      {/* Start markers */}
      <circle cx={xP(2026)} cy={yP(388)} r={5} fill={SE.red} stroke="white" strokeWidth={2} />
      <circle cx={xP(2026)} cy={yP(238)} r={5} fill={SE.green} stroke="white" strokeWidth={2} />
      <text x={xP(2026) - 10} y={yP(388) + 4} textAnchor="end" fill={SE.red}
            fontSize={10} fontWeight="700">$388B</text>
      <text x={xP(2026) - 10} y={yP(238) + 4} textAnchor="end" fill={SE.green}
            fontSize={10} fontWeight="700">$238B</text>

      {/* Right labels — with anti-overlap offsets */}
      {scenarios.map((sc, si) => {
        const isH = hovered === si;
        const lx = xP(2050) + 16;
        const gap = sc.baseEnd - sc.proEnd;
        // Manual y-offsets to prevent SAI Proactive / LTG Baseline overlap
        const baseY = yP(sc.baseEnd);
        const proY = si === 0 ? yP(sc.proEnd) :
                     si === 1 ? yP(sc.proEnd) - 8 :  // SAI Pro: nudge up
                     yP(sc.proEnd);
        const nameY = si === 2 ? yP(sc.baseEnd) + 8 : baseY; // LTG Base: nudge down
        return (
          <g key={`lb${si}`}>
            <text x={lx} y={nameY - 4} fill={sc.color}
                  fontSize={isH ? 12 : 11} fontWeight="700">{sc.abbr}</text>
            <text x={lx} y={nameY + 11} fill={sc.color}
                  fontSize={10} opacity={0.6}>${sc.baseEnd.toLocaleString()}B</text>
            <text x={lx} y={proY + 5} fill={sc.color}
                  fontSize={9} opacity={0.45} fontStyle="italic">
              → ${sc.proEnd.toLocaleString()}B
            </text>
            {isH && (
              <g>
                <line x1={lx + 90} y1={yP(sc.baseEnd) + 6} x2={lx + 90} y2={yP(sc.proEnd) - 4}
                      stroke={sc.color} strokeWidth={1.2} opacity={0.35} />
                <text x={lx + 97} y={(yP(sc.baseEnd) + yP(sc.proEnd)) / 2 + 4}
                      fill={sc.color} fontSize={9.5} fontWeight="600">
                  ${gap.toLocaleString()}B gap
                </text>
              </g>
            )}
          </g>
        );
      })}

      {/* Legend */}
      <g transform={`translate(${pad.l + 14}, ${pad.t + 10})`}>
        <line x1={0} y1={0} x2={18} y2={0} stroke={SE.textSecondary} strokeWidth={2} />
        <text x={24} y={4} fill={SE.textSecondary} fontSize={10}>Baseline</text>
        <line x1={0} y1={22} x2={18} y2={22} stroke={SE.textSecondary} strokeWidth={2} strokeDasharray="5 3" />
        <text x={24} y={26} fill={SE.textSecondary} fontSize={10}>Proactive</text>
        <rect x={0} y={39} width={18} height={10} fill={SE.textSecondary} opacity={0.08} rx={2} />
        <text x={24} y={48} fill={SE.textSecondary} fontSize={10}>Adaptation value</text>
      </g>

      {/* Footer */}
      <text x={W/2} y={H - 10} textAnchor="middle" fill={SE.textMuted} fontSize={9}>
        BAU pathway · Ribbon width = adaptation value · Trajectories between endpoints are indicative
      </text>
    </svg>
  );
}
