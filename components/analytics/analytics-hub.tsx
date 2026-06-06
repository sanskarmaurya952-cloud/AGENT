"use client";

import { ChartCard } from "@/components/dashboard/chart-card";
import { FraudTrendChart } from "@/components/charts/fraud-trend-chart";
import { MemoryGrowthChart } from "@/components/charts/memory-growth-chart";
import { AnalystDecisionsChart } from "@/components/charts/analyst-decisions-chart";
import { RiskDistributionChart } from "@/components/charts/risk-distribution-chart";

export function AnalyticsHub() {
  return (
    <section className="grid gap-5 xl:grid-cols-2">
      <ChartCard title="Fraud Trends" description="Macro trendline for major threat types"><FraudTrendChart /></ChartCard>
      <ChartCard title="Prediction Accuracy" description="Model quality over time"><RiskDistributionChart /></ChartCard>
      <ChartCard title="Investigator Performance" description="Throughput and precision"><AnalystDecisionsChart /></ChartCard>
      <ChartCard title="Memory Effectiveness" description="Memory uplift and retention curve"><MemoryGrowthChart /></ChartCard>
    </section>
  );
}