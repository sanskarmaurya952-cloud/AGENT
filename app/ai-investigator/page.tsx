import { getAlertsData } from "@/lib/api";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { AiInvestigator } from "@/components/ai/ai-investigator";

export default async function AiInvestigatorPage() {
  const alerts = await getAlertsData();

  return (
    <DashboardShell title="AI Investigator" description="Copilot for fraud, AML, and memory-backed case reasoning">
      <AiInvestigator alerts={alerts.items} />
    </DashboardShell>
  );
}