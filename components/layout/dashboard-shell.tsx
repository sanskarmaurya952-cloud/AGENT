"use client";

import { ReactNode, useState } from "react";
import { Sidebar } from "@/components/navigation/sidebar";
import { Topbar } from "@/components/navigation/topbar";
import { cn } from "@/lib/utils";

type Props = {
  title: string;
  description: string;
  children: ReactNode;
};

export function DashboardShell({ title, description, children }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="min-h-screen overflow-hidden">
      <div className="noise fixed inset-0 pointer-events-none opacity-40" />
      <div className="relative flex min-h-screen">
        <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((value) => !value)} />
        <div className={cn("flex min-h-screen flex-1 flex-col transition-all duration-300", collapsed ? "lg:pl-24" : "lg:pl-80")}>
          <Topbar title={title} description={description} />
          <main className="flex-1 px-4 pb-8 pt-4 md:px-6 lg:px-8">
            <div className="mx-auto flex w-full max-w-[1800px] flex-col gap-6">{children}</div>
          </main>
        </div>
      </div>
    </div>
  );
}