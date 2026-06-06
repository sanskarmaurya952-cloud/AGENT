import { DashboardShell } from "@/components/layout/dashboard-shell";
import { UserProfile } from "@/components/profile/user-profile";

export default function UserProfilePage() {
  return (
    <DashboardShell title="User Profile" description="Analyst activity, permissions, and performance">
      <UserProfile />
    </DashboardShell>
  );
}