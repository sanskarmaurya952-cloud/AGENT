import * as React from "react";
import { cn } from "@/lib/utils";

const baseButton = "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 disabled:pointer-events-none disabled:opacity-50";

const variantClasses = {
  default: "bg-cyan-400 text-slate-950 hover:bg-cyan-300",
  secondary: "bg-white/5 text-white hover:bg-white/10",
  outline: "border border-white/10 bg-white/5 text-white hover:bg-white/10",
  ghost: "text-white hover:bg-white/10"
} as const;

const sizeClasses = {
  default: "h-11 px-4 py-2",
  sm: "h-9 px-3",
  lg: "h-12 px-6",
  icon: "h-10 w-10"
} as const;

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variantClasses;
  size?: keyof typeof sizeClasses;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant = "default", size = "default", ...props }, ref) => {
  return <button ref={ref} className={cn(baseButton, variantClasses[variant], sizeClasses[size], className)} {...props} />;
});
Button.displayName = "Button";

export { Button };