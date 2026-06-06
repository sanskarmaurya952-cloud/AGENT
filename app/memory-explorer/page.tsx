import { getMemories } from "@/lib/api";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { MemoryExplorer } from "@/components/memory/memory-explorer";

export default async function MemoryExplorerPage() {
  const memoriesResponse = await getMemories();

  return (
    <DashboardShell title="Memory Explorer" description="Hindsight learning across investigations and outcomes">
      <MemoryExplorer memoryCards={memoriesResponse.items} />
    </DashboardShell>
  );
}