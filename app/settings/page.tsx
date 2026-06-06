import { DashboardShell } from "@/components/layout/dashboard-shell";
import { SettingsPanel } from "@/components/settings/settings-panel";

export default function SettingsPage() {
  return (
    <DashboardShell title="Settings" description="Tune risk policy, automations, and system preferences">
      <SettingsPanel />
    </DashboardShell>
  );
}