"use client";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const data = [
  { type: "Identity", value: 92 },
  { type: "AML", value: 78 },
  { type: "Card", value: 64 },
  { type: "Merchant", value: 56 },
  { type: "Chargeback", value: 48 }
];

export function FraudBreakdownChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
        <XAxis dataKey="type" stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <YAxis stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Bar dataKey="value" radius={[12, 12, 0, 0]} fill="url(#fraudGradient)" />
        <defs>
          <linearGradient id="fraudGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#22d3ee" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
        </defs>
      </BarChart>
    </ResponsiveContainer>
  );
}