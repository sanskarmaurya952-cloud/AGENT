import { DashboardShell } from "@/components/layout/dashboard-shell";
import { KnowledgeGraph } from "@/components/graph/knowledge-graph";

export default function KnowledgeGraphPage() {
  return (
    <DashboardShell title="Knowledge Graph" description="Fraud intelligence relationships and entity linkage">
      <KnowledgeGraph />
    </DashboardShell>
  );
}