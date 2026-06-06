"use client";

import { useMemo, useState } from "react";

const columns = ["New", "Under Review", "Investigating", "Escalated", "Resolved"] as const;

const initial = {
  New: ["Case 449", "Case 450"],
  "Under Review": ["Case 443"],
  Investigating: ["Case 447", "Case 448"],
  Escalated: ["Case 441"],
  Resolved: ["Case 432", "Case 438"]
};

export function CaseManagementBoard() {
  const [board] = useState(initial);
  const content = useMemo(() => board, [board]);

  return (
    <section className="grid gap-4 xl:grid-cols-5">
      {columns.map((column) => (
        <div key={column} className="glass-card gradient-border min-h-[640px] p-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white">{column}</h3>
            <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-xs text-slate-300">{content[column].length}</span>
          </div>
          <div className="mt-4 space-y-3">
            {content[column].map((caseId) => (
              <div key={caseId} className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200 shadow-premium transition hover:-translate-y-1 hover:bg-white/10">
                <p className="text-xs uppercase tracking-[0.25em] text-cyan-200/70">Investigation</p>
                <p className="mt-2 text-lg font-semibold text-white">{caseId}</p>
                <p className="mt-2 text-slate-400">Memory matched to previous fraud family and escalation protocol.</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}