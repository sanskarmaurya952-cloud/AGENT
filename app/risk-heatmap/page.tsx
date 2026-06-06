import { DashboardShell } from "@/components/layout/dashboard-shell";
import { RiskHeatmap } from "@/components/geo/risk-heatmap";

export default function RiskHeatmapPage() {
  return (
    <DashboardShell title="Risk Heatmap" description="Geographic risk hotspots and cross-border transfer pressure">
      <RiskHeatmap />
    </DashboardShell>
  );
}