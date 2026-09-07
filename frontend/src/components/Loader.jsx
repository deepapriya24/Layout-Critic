export default function Loader() {
  return (
    <div className="flex items-center justify-center gap-2 py-8">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-3 h-3 rounded-full bg-accent shadow-glowSm animate-pulseBorder"
          style={{ animationDelay: `${i * 0.2}s` }}
        />
      ))}
      <span className="ml-3 font-mono text-sm text-accent tracking-wide">
        ANALYZING LAYOUT...
      </span>
    </div>
  );
}
