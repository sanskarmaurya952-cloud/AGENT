import { getTransactionsData } from "@/lib/api";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { LiveTransactionsTable } from "@/components/live/live-transactions-table";

export default async function LiveTransactionsPage() {
  const transactions = await getTransactionsData();

  return (
    <DashboardShell title="Live Transactions" description="Real-time monitoring with risk-aware routing">
      <LiveTransactionsTable rows={transactions.items} />
    </DashboardShell>
  );
}