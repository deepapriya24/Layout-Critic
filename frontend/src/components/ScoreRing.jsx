import { useEffect, useState } from "react";

export default function ScoreRing({ score, label, size = 100 }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;

  useEffect(() => {
    const t = setTimeout(() => setAnimatedScore(score), 100);
    return () => clearTimeout(t);
  }, [score]);

  const offset = circumference - (animatedScore / 10) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#1f1f28"
          strokeWidth="6"
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E87A2D"
          strokeWidth="6"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 1s ease-out", filter: "drop-shadow(0 0 4px #E87A2D)" }}
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="middle"
          className="fill-white font-mono"
          fontSize={size * 0.22}
          transform={`rotate(90 ${size / 2} ${size / 2})`}
        >
          {score.toFixed(1)}
        </text>
      </svg>
      {label && <span className="text-xs font-mono text-gray-400 uppercase tracking-wide">{label}</span>}
    </div>
  );
}
