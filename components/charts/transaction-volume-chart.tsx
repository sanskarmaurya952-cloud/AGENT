"use client";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const data = [
  { hour: "00", value: 1800 },
  { hour: "04", value: 1200 },
  { hour: "08", value: 2600 },
  { hour: "12", value: 4200 },
  { hour: "16", value: 3600 },
  { hour: "20", value: 3000 },
  { hour: "24", value: 2800 }
];

export function TransactionVolumeChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data}>
        <defs>
          <linearGradient id="volumeFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.55} />
            <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
        <XAxis dataKey="hour" stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <YAxis stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Area type="monotone" dataKey="value" stroke="#38bdf8" fill="url(#volumeFill)" strokeWidth={3} />
      </AreaChart>
    </ResponsiveContainer>
  );
}