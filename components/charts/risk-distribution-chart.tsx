"use client";

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const data = [
  { name: "Low", value: 36 },
  { name: "Medium", value: 28 },
  { name: "High", value: 22 },
  { name: "Critical", value: 14 }
];

const colors = ["#0ea5e9", "#22c55e", "#f59e0b", "#ef4444"];

export function RiskDistributionChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" innerRadius={62} outerRadius={108} paddingAngle={4}>
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={colors[index]} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}