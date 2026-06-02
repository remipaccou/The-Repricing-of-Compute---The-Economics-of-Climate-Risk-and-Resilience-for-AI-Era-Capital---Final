import { useState } from "react";

const SE = {
  dark: '#0A2F24', green: '#3DCD58', red: '#FF0050',
  amber: '#FFCE00', cyan: '#24F0FF', blue: '#2040FF',
  bg: '#FFFFFF', card: '#FAFAF8', border: '#E5E3DE',
  textPrimary: '#0A2F24', textSecondary: '#6B6860', textMuted: '#A8A49C',
};

const channels = [
  { name: 'Business Interruption', abbr: 'β', base: 121.4, proact: 78.9, color: SE.blue },
  { name: 'Carbon Costs',          abbr: 'CC', base: 107.1, proact: 39.6, color: SE.green },
  { name: 'Physical Damage',       abbr: 'δ', base: 84.1,  proact: 66.4, color: SE.red },
  { name: 'Cooling Stress',        abbr: 'γ', base: 72.6,  proact: 50.8, color: SE.amber },
  { name: 'Heat Productivity',     abbr: 'ξ', base: 2.4,   proact: 1.9,  color: SE.cyan },
];

export default function Butterfly() {
  const [hovered, setHovered] = useState(null);
  const W = 960, H = 600;
  const cx = 480;
  const barH = 24;
  const rowH = 86;
  const topY = 110;
  const maxVal = 125;
  const scale = 290 / maxVal;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', background: SE.bg, fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif" }}>

      {/* Alternating row bands */}
      {channels.map((_, i) => (
        <rect key={`bg${i}`} x={0} y={topY + i * rowH - 16} width={W} height={rowH}
              fill={i % 2 === 0 ? SE.card : SE.bg} />
      ))}

      {/* Headers */}
      <g>
        <text x={cx - 155} y={38} textAnchor="middle" fill={SE.red}
              fontSize={10} fontWeight="600" letterSpacing="2" opacity={0.5}>BASELINE</text>
        <text x={cx - 155} y={62} textAnchor="middle" fill={SE.red}
              fontSize={22} fontWeight="700" opacity={0.45}>$388B</text>
        <text x={cx - 155} y={80} textAnchor="middle" fill={SE.red}
              fontSize={9} opacity={0.25}>← before adaptation</text>

        <text x={cx + 155} y={38} textAnchor="middle" fill={SE.green}
              fontSize={10} fontWeight="600" letterSpacing="2" opacity={0.55}>PROACTIVE</text>
        <text x={cx + 155} y={62} textAnchor="middle" fill={SE.green}
              fontSize={22} fontWeight="700" opacity={0.55}>$238B</text>
        <text x={cx + 155} y={80} textAnchor="middle" fill={SE.green}
              fontSize={9} opacity={0.3}>after adaptation →</text>
      </g>

      {/* Center axis + scale guides */}
      <line x1={cx} y1={90} x2={cx} y2={topY + channels.length * rowH - 24}
            stroke={SE.dark} strokeWidth={1} opacity={0.15} />
      {[50, 100].map(v => {
        const px = v * scale;
        return (
          <g key={v} opacity={0.1}>
            <line x1={cx - px} y1={94} x2={cx - px} y2={topY + channels.length * rowH - 24}
                  stroke={SE.dark} strokeWidth={0.5} strokeDasharray="2 6" />
            <line x1={cx + px} y1={94} x2={cx + px} y2={topY + channels.length * rowH - 24}
                  stroke={SE.dark} strokeWidth={0.5} strokeDasharray="2 6" />
          </g>
        );
      })}

      {/* Channel rows */}
      {channels.map((ch, i) => {
        const y = topY + i * rowH;
        const bw = ch.base * scale;
        const pw = ch.proact * scale;
        const red = Math.round(100 * (1 - ch.proact / ch.base));
        const saved = (ch.base - ch.proact).toFixed(0);
        const isH = hovered === i;
        const barY = y + 14;

        return (
          <g key={i}
             onMouseEnter={() => setHovered(i)}
             onMouseLeave={() => setHovered(null)}
             style={{ cursor: 'pointer' }}>

            {/* Channel label */}
            <text x={cx - bw - 20} y={barY + 7}
                  textAnchor="end" fill={SE.textPrimary} fontSize={13}
                  fontWeight={isH ? '700' : '500'} opacity={isH ? 1 : 0.85}>
              {ch.name}
            </text>
            <text x={cx - bw - 20} y={barY + 22}
                  textAnchor="end" fill={SE.textMuted} fontSize={9.5}>
              {ch.abbr} channel
            </text>

            {/* Baseline bar */}
            <rect x={cx - bw} y={barY} width={bw} height={barH}
                  fill={ch.color} opacity={isH ? 0.22 : 0.12} rx={4} />
            {bw > 35 && (
              <text x={cx - bw + 12} y={barY + barH/2 + 4}
                    fill={ch.color} fontSize={10.5} fontWeight="500" opacity={0.45}>
                ${ch.base.toFixed(0)}B
              </text>
            )}

            {/* Proactive bar */}
            <rect x={cx} y={barY} width={pw} height={barH}
                  fill={ch.color} opacity={isH ? 0.78 : 0.58} rx={4} />
            <text x={cx + pw + 12} y={barY + barH/2 + 4}
                  fill={ch.color} fontSize={11} fontWeight="700"
                  opacity={isH ? 1 : 0.8}>
              ${ch.proact.toFixed(0)}B
            </text>

            {/* Reduction pill — skip for tiny channels */}
            {bw > 20 && (
              <g>
                <rect x={cx - 22} y={barY + barH/2 - 9} width={44} height={18}
                      fill={SE.dark} rx={9} opacity={0.8} />
                <text x={cx} y={barY + barH/2 + 4}
                      textAnchor="middle" fill="white" fontSize={9} fontWeight="700">
                  −{red}%
                </text>
              </g>
            )}

            {/* Hover detail */}
            {isH && ch.base > 5 && (
              <text x={cx} y={barY + barH + 20}
                    textAnchor="middle" fill={ch.color} fontSize={9.5}
                    fontWeight="600" opacity={0.55}>
                ${saved}B protected value
              </text>
            )}
          </g>
        );
      })}

      {/* Footer */}
      <line x1={100} y1={H - 38} x2={W - 100} y2={H - 38}
            stroke={SE.border} strokeWidth={0.5} />
      <text x={cx} y={H - 18} textAnchor="middle" fill={SE.textMuted} fontSize={9}>
        Installed base · BAU/MEAN pathway · All reduction figures net of adaptation cost
      </text>
    </svg>
  );
}
