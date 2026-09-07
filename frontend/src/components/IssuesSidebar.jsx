export default function IssuesSidebar({ issues }) {
  return (
    <div className="flex flex-col gap-3">
      <h3 className="font-mono text-accent text-sm uppercase tracking-wide mb-1">
        Flagged Issues ({issues.length})
      </h3>
      {issues.map((issue, i) => (
        <div
          key={i}
          className="opacity-0 animate-slideIn bg-panel border border-accent/20 rounded-lg p-3 hover:border-accent/60 transition-colors"
          style={{ animationDelay: `${i * 0.1}s` }}
        >
          <p className="text-sm font-medium text-white">{issue.label}</p>
          <p className="text-xs text-gray-400 mt-1">{issue.fix}</p>
        </div>
      ))}
    </div>
  );
}
