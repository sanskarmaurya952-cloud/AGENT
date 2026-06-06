import { DashboardShell } from "@/components/layout/dashboard-shell";
import { AnalyticsHub } from "@/components/analytics/analytics-hub";

export default function AnalyticsPage() {
  return (
    <DashboardShell title="Analytics" description="Business intelligence for risk, accuracy, and memory effectiveness">
      <AnalyticsHub />
    </DashboardShell>
  );
}