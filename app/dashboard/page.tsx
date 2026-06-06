import { StatCard } from "@/components/dashboard/stat-card";
import { ChartCard } from "@/components/dashboard/chart-card";
import { ExecutiveHeader } from "@/components/dashboard/executive-header";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { FraudTrendChart } from "@/components/charts/fraud-trend-chart";
import { RiskDistributionChart } from "@/components/charts/risk-distribution-chart";
import { TransactionVolumeChart } from "@/components/charts/transaction-volume-chart";
import { MemoryGrowthChart } from "@/components/charts/memory-growth-chart";
import { FraudBreakdownChart } from "@/components/charts/fraud-breakdown-chart";
import { AnalystDecisionsChart } from "@/components/charts/analyst-decisions-chart";
import { LearningJourney } from "@/components/dashboard/learning-journey";
import { getDashboardData } from "@/lib/api";

export default async function DashboardPage() {
  const dashboard = await getDashboardData();

  return (
    <DashboardShell title="Dashboard" description="Executive risk overview and memory-aware intelligence">
      <ExecutiveHeader />

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {dashboard.kpis.map((item, index) => (
          <StatCard key={item.label} item={item} index={index} />
        ))}
      </section>

      <section className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Fraud Trend" description="Monthly fraud growth and anomaly spikes" className="xl:col-span-2">
          <FraudTrendChart />
        </ChartCard>
        <ChartCard title="Risk Distribution" description="Portfolio-wide risk mix">
          <RiskDistributionChart />
        </ChartCard>
      </section>

      <section className="grid gap-5 xl:grid-cols-3">
        <ChartCard title="Transaction Volume" description="Real-time intake and velocity">
          <TransactionVolumeChart />
        </ChartCard>
        <ChartCard title="Memory Growth" description="Knowledge accumulation over time">
          <MemoryGrowthChart />
        </ChartCard>
        <ChartCard title="Fraud Categories" description="Case mix by attack pattern">
          <FraudBreakdownChart />
        </ChartCard>
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.3fr_0.7fr]">
        <ChartCard title="Analyst Decisions" description="Human-in-the-loop outcomes and SLA performance" className="min-h-[380px]">
          <AnalystDecisionsChart />
        </ChartCard>
        <LearningJourney />
      </section>
    </DashboardShell>
  );
}