import { useState } from "react";

const SE = {
  dark: '#0A2F24', green: '#3DCD58', red: '#FF0050',
  amber: '#FFCE00', cyan: '#24F0FF', blue: '#2040FF',
  bg: '#FFFFFF', border: '#E5E3DE', textPrimary: '#0A2F24',
  textSecondary: '#6B6860', textMuted: '#A8A49C',
};

const channels = ['Business Interruption', 'Cooling', 'Physical Damage', 'Carbon'];
const angles = [0, 90, 180, 270];

const regions = [
  { name: 'United States', vals: [44, 25, 19, 11], color: SE.blue },
  { name: 'Europe',        vals: [24, 21, 11, 42], color: SE.green },
  { name: 'China',         vals: [28,  9, 30, 32], color: SE.red },
  { name: 'APMEA',         vals: [26, 19, 29, 24], color: SE.amber },
];

function polar(cx, cy, r, deg) {
  const a = (deg - 90) * Math.PI / 180;
  return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
}

export default function Radar() {
  const [hovered, setHovered] = useState(null);
  const W = 820, H = 840;
  const cx = 380, cy = 370;
  const R = 255;
  const gridLevels = [10, 20, 30, 40, 50];

  const labelCfg = [
    { dx: 0, dy: -24, anchor: 'middle' },
    { dx: 26, dy: 5, anchor: 'start' },
    { dx: 0, dy: 30, anchor: 'middle' },
    { dx: -26, dy: 5, anchor: 'end' },
  ];

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', background: SE.bg, fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif" }}>

      {/* Polygon grid */}
      {gridLevels.map(pct => {
        const r = R * pct / 50;
        const pts = angles.map(a => { const p = polar(cx, cy, r, a); return `${p.x},${p.y}`; }).join(' ');
        return <polygon key={pct} points={pts} fill="none" stroke={SE.border} strokeWidth={0.7} />;
      })}

      {/* Axis lines */}
      {angles.map((a, i) => {
        const p = polar(cx, cy, R + 8, a);
        return <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke={SE.border} strokeWidth={0.7} />;
      })}

      {/* Grid % labels */}
      {gridLevels.map(pct => (
        <text key={`g${pct}`} x={cx + 8} y={cy - R * pct / 50 - 5}
              fill={SE.textMuted} fontSize={9.5}>{pct}%</text>
      ))}

      {/* Channel labels — generous distance from polygon */}
      {channels.map((ch, i) => {
        const p = polar(cx, cy, R + 48, angles[i]);
        const cfg = labelCfg[i];
        return (
          <text key={`c${i}`} x={p.x + cfg.dx} y={p.y + cfg.dy}
                textAnchor={cfg.anchor} dominantBaseline="middle"
                fill={SE.textPrimary} fontSize={13} fontWeight="600">
            {ch}
          </text>
        );
      })}

      {/* Region polygons */}
      {regions.map((reg, ri) => {
        const isH = hovered === reg.name;
        const pts = reg.vals.map((v, i) => {
          const p = polar(cx, cy, R * v / 50, angles[i]);
          return `${p.x},${p.y}`;
        }).join(' ');

        return (
          <g key={ri}
             onMouseEnter={() => setHovered(reg.name)}
             onMouseLeave={() => setHovered(null)}
             style={{ cursor: 'pointer' }}>
            <polygon points={pts}
                     fill={reg.color} fillOpacity={isH ? 0.14 : 0.05}
                     stroke={reg.color} strokeWidth={isH ? 3 : 2}
                     strokeOpacity={isH ? 1 : 0.7}
                     strokeLinejoin="round" />
            {reg.vals.map((v, i) => {
              const p = polar(cx, cy, R * v / 50, angles[i]);
              return (
                <circle key={i} cx={p.x} cy={p.y} r={isH ? 6 : 4}
                        fill={reg.color} stroke="white" strokeWidth={2} />
              );
            })}
            {isH && reg.vals.map((v, i) => {
              const p2 = polar(cx, cy, R * v / 50 + 22, angles[i]);
              return (
                <g key={`v${i}`}>
                  <rect x={p2.x - 20} y={p2.y - 11} width={40} height={20}
                        fill={reg.color} rx={10} opacity={0.88} />
                  <text x={p2.x} y={p2.y + 4} textAnchor="middle"
                        fill="white" fontSize={10} fontWeight="700">{v}%</text>
                </g>
              );
            })}
          </g>
        );
      })}

      {/* Legend */}
      <g transform="translate(640, 60)">
        <text x={0} y={-14} fill={SE.textMuted} fontSize={9.5} fontWeight="600" letterSpacing="1.2">
          REGIONS
        </text>
        {regions.map((reg, i) => {
          const isH = hovered === reg.name;
          return (
            <g key={i} transform={`translate(0, ${i * 36})`}
               onMouseEnter={() => setHovered(reg.name)}
               onMouseLeave={() => setHovered(null)}
               style={{ cursor: 'pointer' }}>
              <rect x={0} y={-2} width={20} height={4} fill={reg.color} rx={2}
                    opacity={isH ? 0.9 : 0.55} />
              <circle cx={10} cy={0} r={4.5} fill={reg.color} stroke="white" strokeWidth={1.5}
                      opacity={isH ? 1 : 0.7} />
              <text x={30} y={4} fill={isH ? SE.textPrimary : SE.textSecondary}
                    fontSize={12} fontWeight={isH ? '700' : '400'}>{reg.name}</text>
            </g>
          );
        })}
      </g>

      {/* Footer — well below Physical Damage */}
      <line x1={120} y1={H - 48} x2={W - 120} y2={H - 48}
            stroke={SE.border} strokeWidth={0.5} />
      <text x={cx} y={H - 24} textAnchor="middle" fill={SE.textMuted} fontSize={9}>
        Channel share as % of regional ClimVaR · BAU/MEAN · Installed base
      </text>
    </svg>
  );
}
