"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const data = [
  { month: "Jan", value: 42 },
  { month: "Feb", value: 54 },
  { month: "Mar", value: 61 },
  { month: "Apr", value: 72 },
  { month: "May", value: 83 },
  { month: "Jun", value: 96 }
];

export function FraudTrendChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
        <XAxis dataKey="month" stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <YAxis stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Line type="monotone" dataKey="value" stroke="#22d3ee" strokeWidth={3} dot={{ r: 4, fill: "#22d3ee" }} activeDot={{ r: 7 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}