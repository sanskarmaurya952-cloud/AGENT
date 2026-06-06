import { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function ChartCard({ title, description, children, className }: { title: string; description: string; children: ReactNode; className?: string }) {
  return (
    <section className={cn("glass-card gradient-border p-5", className)}>
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <p className="text-sm text-slate-400">{description}</p>
      </div>
      <div className="h-[320px] w-full">{children}</div>
    </section>
  );
}