"use client";

import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

type Stat = { label: string; value: string; delta: string; tone: string };

export function StatCard({ item, index }: { item: Stat; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay: index * 0.05 }}
      className="glass-card gradient-border overflow-hidden p-5"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm text-slate-400">{item.label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-white">{item.value}</p>
        </div>
        <div className={cn("rounded-2xl border px-3 py-2 text-xs font-semibold uppercase tracking-[0.2em]", item.tone === "cyan" && "border-cyan-400/30 bg-cyan-400/10 text-cyan-100", item.tone === "emerald" && "border-emerald-400/30 bg-emerald-400/10 text-emerald-100", item.tone === "amber" && "border-amber-400/30 bg-amber-400/10 text-amber-100", item.tone === "blue" && "border-blue-400/30 bg-blue-400/10 text-blue-100", item.tone === "violet" && "border-violet-400/30 bg-violet-400/10 text-violet-100", item.tone === "green" && "border-green-400/30 bg-green-400/10 text-green-100", item.tone === "teal" && "border-teal-400/30 bg-teal-400/10 text-teal-100", item.tone === "slate" && "border-slate-400/30 bg-slate-400/10 text-slate-100")}>
          {item.delta}
        </div>
      </div>
      <div className="mt-6 flex items-center gap-2 text-sm text-slate-400">
        <ArrowUpRight className="h-4 w-4 text-cyan-300" />
        AI memory-adjusted signal
      </div>
    </motion.div>
  );
}