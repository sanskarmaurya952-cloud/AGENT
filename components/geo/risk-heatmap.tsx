"use client";

import { motion } from "framer-motion";
import { Globe2, MapPinned } from "lucide-react";

const markers = [
  { top: "28%", left: "18%", color: "bg-cyan-400" },
  { top: "35%", left: "42%", color: "bg-red-400" },
  { top: "52%", left: "67%", color: "bg-amber-400" },
  { top: "63%", left: "24%", color: "bg-emerald-400" },
  { top: "41%", left: "78%", color: "bg-red-400" }
];

export function RiskHeatmap() {
  return (
    <section className="grid gap-5 xl:grid-cols-[1.4fr_0.6fr]">
      <div className="glass-card gradient-border relative h-[760px] overflow-hidden p-5">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_35%,rgba(34,211,238,0.14),transparent_15%),radial-gradient(circle_at_65%_45%,rgba(239,68,68,0.14),transparent_16%),radial-gradient(circle_at_50%_70%,rgba(16,185,129,0.12),transparent_14%)]" />
        <div className="relative flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white">Global Fraud Hotspots</h3>
            <p className="text-sm text-slate-400">Animated indicators across suspicious geographies</p>
          </div>
          <div className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.25em] text-slate-300">
            <Globe2 className="mr-2 inline h-3.5 w-3.5" /> Live map
          </div>
        </div>
        <div className="relative mt-5 h-[680px] rounded-[2rem] border border-white/10 bg-slate-950/60">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.03),transparent_55%)]" />
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:80px_80px] opacity-30" />
          {markers.map((marker, index) => (
            <motion.div key={index} animate={{ scale: [1, 1.15, 1], opacity: [0.75, 1, 0.75] }} transition={{ duration: 2.6 + index * 0.2, repeat: Infinity }} className={`absolute h-4 w-4 rounded-full ${marker.color} shadow-[0_0_30px_currentColor]`} style={{ top: marker.top, left: marker.left }}>
              <span className="absolute inset-0 rounded-full border border-current/40 animate-ping" />
            </motion.div>
          ))}
          <div className="absolute bottom-5 left-5 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
            Suspicious transfer density increases near financial gateways.
          </div>
        </div>
      </div>

      <div className="glass-card gradient-border p-5">
        <h3 className="text-lg font-semibold text-white">High-Risk Regions</h3>
        <div className="mt-4 space-y-3">
          {[
            "Singapore corridor",
            "London fintech cluster",
            "Dubai payment network",
            "Mexico City mule route",
            "New York merchant burst"
          ].map((region) => (
            <div key={region} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
              <span className="flex items-center gap-2"><MapPinned className="h-4 w-4 text-cyan-300" />{region}</span>
              <span className="text-xs uppercase tracking-[0.2em] text-amber-200">Watchlist</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}