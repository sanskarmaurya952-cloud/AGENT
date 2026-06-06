"use client";

import { useState, useEffect } from "react";
import { Search, Filter, Layers3, BrainCog, ChevronDown, Loader2, AlertCircle } from "lucide-react";
import { searchMemory, type MemoryItem } from "@/lib/api";

type Props = {
  memoryCards: MemoryItem[];
};

const RISK_LEVELS = ["Critical", "High", "Medium", "Low"];
const FRAUD_TYPES = ["Identity Fraud", "Merchant Abuse", "Money Laundering", "Card Fraud", "Account Takeover"];
const CONFIDENCE_RANGES = [
  { label: "90-100%", min: 0.9, max: 1.0 },
  { label: "80-89%", min: 0.8, max: 0.89 },
  { label: "70-79%", min: 0.7, max: 0.79 },
  { label: "Below 70%", min: 0, max: 0.69 },
];

export function MemoryExplorer({ memoryCards: initialMemories }: Props) {
  const [memories, setMemories] = useState<MemoryItem[]>(initialMemories);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);

  // Filters
  const [selectedRiskLevels, setSelectedRiskLevels] = useState<string[]>([]);
  const [selectedFraudTypes, setSelectedFraudTypes] = useState<string[]>([]);
  const [selectedConfidenceRange, setSelectedConfidenceRange] = useState<string | null>(null);

  // Search memories
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setMemories(initialMemories);
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const result = await searchMemory(searchQuery, 25);
      setMemories(result.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to search memories");
      setMemories([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Apply filters
  const filteredMemories = memories.filter((memory) => {
    if (selectedRiskLevels.length > 0 && !selectedRiskLevels.includes(memory.riskLevel)) {
      return false;
    }
    if (selectedFraudTypes.length > 0 && !selectedFraudTypes.includes(memory.fraudType)) {
      return false;
    }
    if (selectedConfidenceRange) {
      const range = CONFIDENCE_RANGES.find((r) => r.label === selectedConfidenceRange);
      if (range && (memory.confidence < range.min || memory.confidence > range.max)) {
        return false;
      }
    }
    return true;
  });

  const toggleRiskLevel = (level: string) => {
    setSelectedRiskLevels((prev) =>
      prev.includes(level) ? prev.filter((l) => l !== level) : [...prev, level]
    );
  };

  const toggleFraudType = (type: string) => {
    setSelectedFraudTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  };

  return (
    <section className="space-y-5">
      <div className="glass-card gradient-border p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs uppercase tracking-[0.25em] text-cyan-100">
              <BrainCog className="h-3.5 w-3.5" />
              Hindsight Memory
            </div>
            <h3 className="mt-4 text-2xl font-semibold text-white">Memory Timeline</h3>
            <p className="mt-2 text-sm text-slate-400">Discover how prior investigations inform present decisions.</p>
          </div>
          <div className="flex gap-3">
            <form onSubmit={handleSearch} className="relative w-72 max-w-full">
              <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="h-11 w-full rounded-xl border border-white/10 bg-white/5 pl-11 text-sm text-white placeholder:text-slate-500 outline-none transition focus:border-cyan-400/50 focus:bg-white/10"
                placeholder="Search memories, cases, fraud types..."
              />
            </form>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="inline-flex h-11 items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm text-white hover:bg-white/10 transition"
            >
              <Filter className="h-4 w-4" />
              Filter
              {showFilters && <ChevronDown className="h-4 w-4" />}
            </button>
          </div>
        </div>

        {showFilters && (
          <div className="mt-6 grid gap-6 md:grid-cols-3 border-t border-white/10 pt-6">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Risk Level</h4>
              <div className="mt-3 space-y-2">
                {RISK_LEVELS.map((level) => (
                  <label key={level} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedRiskLevels.includes(level)}
                      onChange={() => toggleRiskLevel(level)}
                      className="h-4 w-4 rounded border-white/20 bg-white/5 text-cyan-500 cursor-pointer"
                    />
                    <span className="text-sm text-slate-300">{level}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Fraud Type</h4>
              <div className="mt-3 space-y-2">
                {FRAUD_TYPES.map((type) => (
                  <label key={type} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedFraudTypes.includes(type)}
                      onChange={() => toggleFraudType(type)}
                      className="h-4 w-4 rounded border-white/20 bg-white/5 text-cyan-500 cursor-pointer"
                    />
                    <span className="text-sm text-slate-300">{type}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Confidence</h4>
              <div className="mt-3 space-y-2">
                {CONFIDENCE_RANGES.map((range) => (
                  <label key={range.label} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="confidence"
                      checked={selectedConfidenceRange === range.label}
                      onChange={() => setSelectedConfidenceRange(range.label)}
                      className="h-4 w-4 border-white/20 bg-white/5 text-cyan-500 cursor-pointer"
                    />
                    <span className="text-sm text-slate-300">{range.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="glass-card gradient-border border-red-500/20 bg-red-500/10 p-5 flex gap-3">
          <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-red-200">{error}</p>
            <p className="text-xs text-red-300/70 mt-1">Try again or refine your search</p>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="glass-card gradient-border p-12 flex flex-col items-center justify-center gap-4">
          <Loader2 className="h-8 w-8 text-cyan-400 animate-spin" />
          <p className="text-sm text-slate-300">Searching memories...</p>
        </div>
      )}

      {!isLoading && filteredMemories.length === 0 && (
        <div className="glass-card gradient-border p-12 text-center">
          <Layers3 className="h-12 w-12 text-slate-600 mx-auto mb-4 opacity-50" />
          <p className="text-slate-300">No memories found</p>
          <p className="text-sm text-slate-500 mt-1">
            {searchQuery ? "Try a different search query" : "Memories will appear here when cases are investigated"}
          </p>
        </div>
      )}

      <div className="grid gap-5 xl:grid-cols-2">
        {filteredMemories.map((memory) => (
          <article
            key={memory.id}
            className="glass-card gradient-border p-5 transition hover:-translate-y-1 hover:bg-white/[0.06]"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-200/70">{memory.fraudType}</p>
                <h4 className="mt-2 text-xl font-semibold text-white">{memory.title}</h4>
              </div>
              <span className="rounded-full border border-red-400/20 bg-red-400/10 px-3 py-1 text-xs uppercase tracking-[0.25em] text-red-100 flex-shrink-0">
                {memory.riskLevel}
              </span>
            </div>
            <p className="mt-3 text-sm text-slate-300 line-clamp-2">{memory.content}</p>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Confidence</p>
                <p className="mt-2 text-2xl font-semibold text-white">{Math.round(memory.confidence * 100)}%</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Date</p>
                <p className="mt-2 text-2xl font-semibold text-white">
                  {new Date(memory.createdAt).toLocaleDateString()}
                </p>
              </div>
              {memory.learningImpact && (
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4 md:col-span-2">
                  <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Learning Impact</p>
                  <p className="mt-2 text-sm text-slate-200">{memory.learningImpact}</p>
                </div>
              )}
            </div>
          </article>
        ))}
      </div>

      {filteredMemories.length > 0 && (
        <div className="glass-card gradient-border p-5">
          <h3 className="text-lg font-semibold text-white">Results Summary</h3>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Total Memories</p>
              <p className="mt-2 text-3xl font-bold text-cyan-400">{filteredMemories.length}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Avg Confidence</p>
              <p className="mt-2 text-3xl font-bold text-cyan-400">
                {Math.round(
                  (filteredMemories.reduce((sum, m) => sum + m.confidence, 0) / filteredMemories.length) * 100
                )}%
              </p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Critical Cases</p>
              <p className="mt-2 text-3xl font-bold text-red-400">
                {filteredMemories.filter((m) => m.riskLevel === "Critical").length}
              </p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}