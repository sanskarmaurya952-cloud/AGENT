"use client";

export function SettingsPanel() {
  return (
    <section className="grid gap-5 xl:grid-cols-2">
      {[
        "Risk policy thresholds",
        "Alert routing rules",
        "Model memory retention",
        "Investigation permissions"
      ].map((title) => (
        <div key={title} className="glass-card gradient-border p-5">
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <p className="mt-2 text-sm text-slate-400">Premium enterprise control surface ready for demo configuration.</p>
          <div className="mt-4 h-44 rounded-2xl border border-white/10 bg-white/5" />
        </div>
      ))}
    </section>
  );
}