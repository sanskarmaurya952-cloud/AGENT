"use client";

import { motion } from "framer-motion";
import type { TransactionRow } from "@/lib/api";
import { cn } from "@/lib/utils";

const riskClass: Record<string, string> = {
  Low: "border-emerald-400/20 bg-emerald-400/10 text-emerald-100",
  Medium: "border-amber-400/20 bg-amber-400/10 text-amber-100",
  High: "border-orange-400/20 bg-orange-400/10 text-orange-100",
  Critical: "border-red-400/30 bg-red-400/15 text-red-100 shadow-[0_0_24px_rgba(248,113,113,0.35)]"
};

export function LiveTransactionsTable({ rows }: { rows: TransactionRow[] }) {
  return (
    <section className="glass-card gradient-border overflow-hidden">
      <div className="border-b border-white/10 px-5 py-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-semibold text-white">Real-Time Transaction Stream</h3>
            <p className="text-sm text-slate-400">Production-like live feed with risk-aware alerting</p>
          </div>
          <div className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs uppercase tracking-[0.3em] text-cyan-100">
            1,248 events/min
          </div>
        </div>
      </div>
      <div className="overflow-x-auto scrollbar">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-white/[0.03] text-slate-400">
            <tr>
              {[
                "Transaction ID",
                "Customer",
                "Amount",
                "Location",
                "Merchant",
                "Risk Score",
                "Status",
                "Action"
              ].map((column) => (
                <th key={column} className="px-5 py-4 font-medium tracking-wide">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <motion.tr
                key={row.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="border-t border-white/5 text-slate-200 hover:bg-white/[0.03]"
              >
                <td className="px-5 py-4 font-medium text-white">{row.id}</td>
                <td className="px-5 py-4">{row.customer}</td>
                <td className="px-5 py-4">
                  {row.currency} {row.amount.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                </td>
                <td className="px-5 py-4">{row.location}</td>
                <td className="px-5 py-4">{row.merchant}</td>
                <td className="px-5 py-4">{row.riskScore}</td>
                <td className="px-5 py-4">
                  <span className={cn("rounded-full border px-3 py-1 text-xs uppercase tracking-[0.2em]", riskClass[row.risk])}>{row.status}</span>
                </td>
                <td className="px-5 py-4">
                  <button className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs text-white transition hover:bg-white/10">{row.action}</button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}