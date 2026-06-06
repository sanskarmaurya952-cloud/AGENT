"use client";

import { motion } from "framer-motion";
import { Sparkles, ShieldCheck } from "lucide-react";

export function ExecutiveHeader() {
  return (
    <section className="glass-card gradient-border relative overflow-hidden p-6 md:p-8">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.18),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(59,130,246,0.14),transparent_26%)]" />
      <div className="relative flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/25 bg-cyan-400/10 px-4 py-2 text-xs uppercase tracking-[0.3em] text-cyan-100">
            <Sparkles className="h-3.5 w-3.5" />
            Memory-Powered Intelligence
          </div>
          <h1 className="mt-5 text-4xl font-semibold tracking-tight text-white md:text-5xl xl:text-6xl">Financial Risk Intelligence Center</h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300 md:text-lg">AI-powered fraud detection with memory-based learning for bankers, investigators, compliance teams, and risk leaders.</p>
        </div>

        <motion.div
          initial={{ opacity: 0, x: 16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.55 }}
          className="rounded-3xl border border-emerald-400/20 bg-emerald-400/10 px-5 py-4 text-emerald-100 shadow-glow"
        >
          <div className="flex items-center gap-2 text-sm font-medium">
            <ShieldCheck className="h-4 w-4" />
            Live model health 99.2%
          </div>
          <p className="mt-2 text-sm text-emerald-50/80">Memory reinforcement active across 14 decision loops.</p>
        </motion.div>
      </div>
    </section>
  );
}