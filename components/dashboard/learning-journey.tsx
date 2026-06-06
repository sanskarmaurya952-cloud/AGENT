"use client";

import { motion } from "framer-motion";

const steps = [
  { label: "Interaction 1", title: "Generic Analysis", value: 20 },
  { label: "Interaction 5", title: "Memory Assisted Analysis", value: 58 },
  { label: "Interaction 20", title: "Expert Analysis", value: 92 }
];

export function LearningJourney() {
  return (
    <section className="glass-card gradient-border p-5">
      <h3 className="text-lg font-semibold text-white">AI Learning Journey</h3>
      <p className="mt-1 text-sm text-slate-400">From generic reasoning to expert-level, memory-backed decisions.</p>
      <div className="mt-6 space-y-5">
        {steps.map((step, index) => (
          <motion.div key={step.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.15 }} className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center justify-between text-sm">
              <div>
                <p className="text-cyan-100">{step.label}</p>
                <p className="text-slate-400">{step.title}</p>
              </div>
              <p className="text-lg font-semibold text-white">{step.value}%</p>
            </div>
            <div className="mt-3 h-2 rounded-full bg-white/5">
              <div className="h-2 rounded-full bg-gradient-to-r from-cyan-400 via-blue-400 to-emerald-400" style={{ width: `${step.value}%` }} />
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}