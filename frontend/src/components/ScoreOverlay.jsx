import { useState } from "react";

export default function ScoreOverlay({ imageUrl, issues }) {
  const [hoveredIndex, setHoveredIndex] = useState(null);

  return (
    <div className="relative rounded-xl overflow-hidden border border-accent/30 shadow-glowSm">
      <img src={imageUrl} alt="analyzed layout" className="w-full h-auto block" />

      {issues.map((issue, i) => (
        <div
          key={i}
          onMouseEnter={() => setHoveredIndex(i)}
          onMouseLeave={() => setHoveredIndex(null)}
          className="absolute border-2 border-dashed border-accent animate-pulseBorder cursor-pointer"
          style={{
            left: `${issue.x * 100}%`,
            top: `${issue.y * 100}%`,
            width: `${issue.w * 100}%`,
            height: `${issue.h * 100}%`,
          }}
        >
          {hoveredIndex === i && (
            <div className="absolute -top-2 left-0 -translate-y-full bg-panel border border-accent text-xs font-mono px-2 py-1 rounded shadow-glowSm whitespace-nowrap z-10">
              <p className="text-accent">{issue.label}</p>
              <p className="text-gray-300">{issue.fix}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
