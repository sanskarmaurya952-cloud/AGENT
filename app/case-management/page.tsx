import { DashboardShell } from "@/components/layout/dashboard-shell";
import { CaseManagementBoard } from "@/components/case/case-management-board";

export default function CaseManagementPage() {
  return (
    <DashboardShell title="Case Management" description="Investigation workflow and escalation board">
      <CaseManagementBoard />
    </DashboardShell>
  );
}