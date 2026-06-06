"use client";

import { Search, Bell, ShieldAlert, Sparkles, CircleDot, MoonStar } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ThemeToggle } from "@/components/navigation/theme-toggle";

type Props = { title: string; description: string };

export function Topbar({ title, description }: Props) {
  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/50 backdrop-blur-2xl">
      <div className="flex flex-col gap-4 px-4 py-4 md:px-6 lg:px-8 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.35em] text-cyan-300/70">
            <CircleDot className="h-3 w-3 animate-pulse text-emerald-400" />
            System status live
          </div>
          <h2 className="mt-2 text-2xl font-semibold text-white">{title}</h2>
          <p className="mt-1 text-sm text-slate-400">{description}</p>
        </div>

        <div className="flex flex-1 flex-col gap-3 xl:max-w-[980px] xl:flex-row xl:items-center xl:justify-end">
          <div className="relative w-full xl:max-w-[360px]">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
            <Input className="h-12 rounded-2xl border-white/10 bg-white/5 pl-11 text-white placeholder:text-slate-500" placeholder="Global search across cases, memories, customers..." />
          </div>
          <Button className="h-12 rounded-2xl bg-cyan-400 px-5 text-slate-950 hover:bg-cyan-300">
            <Sparkles className="mr-2 h-4 w-4" />
            AI Assistant
          </Button>
          <div className="flex items-center gap-2">
            <Button variant="outline" className="h-12 rounded-2xl border-white/10 bg-white/5 text-white hover:bg-white/10">
              <ShieldAlert className="mr-2 h-4 w-4 text-amber-300" />
              Risk Alerts
            </Button>
            <Button variant="outline" size="icon" className="h-12 w-12 rounded-2xl border-white/10 bg-white/5 text-white hover:bg-white/10">
              <Bell className="h-4 w-4" />
            </Button>
            <ThemeToggle />
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
              <Avatar className="h-9 w-9 border border-cyan-400/30">
                <AvatarFallback className="bg-cyan-400/15 text-cyan-100">AR</AvatarFallback>
              </Avatar>
              <div className="hidden md:block">
                <p className="text-sm font-medium text-white">Ava Rhodes</p>
                <p className="text-xs text-slate-400">Lead Risk Analyst</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}