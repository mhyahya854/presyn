import React from "react";

interface EmptyStateProps {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  plannedPhase?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  plannedPhase,
}) => {
  return (
    <div className="panel border border-slate-800 bg-[#111726] rounded p-12 text-center max-w-2xl mx-auto my-8">
      <div className="inline-flex items-center justify-center w-12 h-12 rounded bg-slate-900 border border-slate-800 text-slate-400 mb-4">
        <Icon className="w-6 h-6 text-slate-400" />
      </div>
      <h2 className="text-base font-semibold text-slate-100 tracking-tight mb-2">
        {title}
      </h2>
      <p className="text-sm text-slate-400 max-w-md mx-auto leading-relaxed mb-6">
        {description}
      </p>
      {plannedPhase && (
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-slate-900 border border-slate-800 text-xs text-slate-400 font-mono">
          <span className="w-1.5 h-1.5 rounded-sm bg-blue-500"></span>
          <span>Target Architecture: {plannedPhase}</span>
        </div>
      )}
    </div>
  );
};
