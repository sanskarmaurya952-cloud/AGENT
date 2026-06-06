"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export function UserProfile() {
  return (
    <section className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr]">
      <div className="glass-card gradient-border p-6">
        <div className="flex items-center gap-4">
          <Avatar className="h-16 w-16 border border-cyan-400/20">
            <AvatarFallback className="bg-cyan-400/10 text-xl text-cyan-100">AR</AvatarFallback>
          </Avatar>
          <div>
            <h3 className="text-2xl font-semibold text-white">Ava Rhodes</h3>
            <p className="text-slate-400">Lead Risk Analyst</p>
          </div>
        </div>
        <div className="mt-6 space-y-3 text-sm text-slate-300">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Cases reviewed: 624</div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Memory contributions: 91</div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Escalation precision: 97.4%</div>
        </div>
      </div>
      <div className="glass-card gradient-border p-6">
        <h3 className="text-lg font-semibold text-white">Profile Activity</h3>
        <div className="mt-4 h-[400px] rounded-2xl border border-white/10 bg-white/5" />
      </div>
    </section>
  );
}