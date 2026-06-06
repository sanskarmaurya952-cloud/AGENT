"use client";

import { ResponsiveContainer, ComposedChart, Line, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const data = [
  { week: "W1", approvals: 44, accuracy: 78 },
  { week: "W2", approvals: 52, accuracy: 82 },
  { week: "W3", approvals: 58, accuracy: 86 },
  { week: "W4", approvals: 66, accuracy: 90 },
  { week: "W5", approvals: 71, accuracy: 94 }
];

export function AnalystDecisionsChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={data}>
        <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
        <XAxis dataKey="week" stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <YAxis stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Bar dataKey="approvals" fill="#38bdf8" radius={[8, 8, 0, 0]} />
        <Line type="monotone" dataKey="accuracy" stroke="#34d399" strokeWidth={3} dot={{ r: 4 }} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}