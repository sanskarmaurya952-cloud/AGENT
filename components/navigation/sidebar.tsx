"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Banknote, BellRing, ChevronLeft, ChevronRight, Database, Gauge, GitGraph, HeartPulse, LayoutDashboard, Layers3, Search, Shield, Sparkles, UserCircle2, Workflow } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/live-transactions", label: "Live Transactions", icon: Banknote },
  { href: "/case-management", label: "Fraud Investigations", icon: Shield },
  { href: "/ai-investigator", label: "AI Investigator", icon: Sparkles },
  { href: "/memory-explorer", label: "Memory Explorer", icon: Database },
  { href: "/knowledge-graph", label: "Knowledge Graph", icon: GitGraph },
  { href: "/risk-heatmap", label: "Risk Heatmap", icon: HeartPulse },
  { href: "/case-management", label: "Case Management", icon: Layers3 },
  { href: "/analytics", label: "Analytics", icon: Gauge },
  { href: "/settings", label: "Settings", icon: BellRing },
  { href: "/user-profile", label: "User Profile", icon: UserCircle2 }
];

type Props = { collapsed: boolean; onToggle: () => void };

export function Sidebar({ collapsed, onToggle }: Props) {
  const pathname = usePathname();

  return (
    <aside className={cn("fixed left-0 top-0 z-40 hidden h-screen border-r border-white/10 bg-slate-950/80 backdrop-blur-2xl lg:flex", collapsed ? "w-24" : "w-80")}>
      <div className="flex w-full flex-col gap-6 p-4">
        <div className="glass-panel flex items-center justify-between rounded-3xl px-4 py-4">
          {!collapsed && (
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-cyan-300/70">Intelligence Agent</p>
              <h1 className="mt-1 text-lg font-semibold text-white">Memory Risk OS</h1>
            </div>
          )}
          <Button variant="ghost" size="icon" className="rounded-2xl border border-white/10 bg-white/5 text-white hover:bg-white/10" onClick={onToggle}>
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        </div>

        <div className="rounded-3xl border border-cyan-400/20 bg-cyan-400/5 p-4 shadow-glow">
          {!collapsed ? (
            <>
              <p className="text-xs uppercase tracking-[0.3em] text-cyan-200/70">System intelligence</p>
              <p className="mt-2 text-sm text-slate-300">21 active risk models, 4 memory clusters, 99.2% uptime</p>
            </>
          ) : (
            <Search className="mx-auto h-5 w-5 text-cyan-300" />
          )}
        </div>

        <nav className="flex-1 space-y-2 overflow-y-auto pr-1 scrollbar">
          {navItems.map((item) => {
            const active = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link key={item.href} href={item.href} className={cn("group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-all", active ? "bg-cyan-400/10 text-cyan-100 ring-1 ring-cyan-400/30" : "text-slate-300 hover:bg-white/5 hover:text-white")}>
                <motion.span whileHover={{ scale: 1.05 }} className={cn("flex h-10 w-10 items-center justify-center rounded-xl border", active ? "border-cyan-400/30 bg-cyan-400/15" : "border-white/10 bg-white/5")}>
                  <Icon className="h-4 w-4" />
                </motion.span>
                {!collapsed && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        <div className="glass-panel rounded-3xl p-4">
          {!collapsed ? (
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-emerald-300/70">Analyst mode</p>
              <p className="mt-2 text-sm text-slate-300">Premium live triage enabled</p>
            </div>
          ) : (
            <Workflow className="mx-auto h-5 w-5 text-emerald-300" />
          )}
        </div>
      </div>
    </aside>
  );
}