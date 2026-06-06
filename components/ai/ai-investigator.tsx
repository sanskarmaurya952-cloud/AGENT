"use client";

import { useState } from "react";
import { Send, Sparkles, BrainCircuit, AlertTriangle, Loader2, CheckCircle, ThumbsUp, ThumbsDown } from "lucide-react";
import { investigateTransaction, submitAnalystFeedback, type AlertItem, type TransactionRow } from "@/lib/api";

type Props = {
  alerts: AlertItem[];
};

export function AiInvestigator({ alerts }: Props) {
  const [selectedAlert, setSelectedAlert] = useState<string | null>(null);
  const [investigation, setInvestigation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);
  const [feedbackSuccess, setFeedbackSuccess] = useState<string | null>(null);
  const [selectedTransaction, setSelectedTransaction] = useState<TransactionRow | null>(null);

  const mockTransactions: TransactionRow[] = [
    {
      id: "txn_1001",
      customer: "Nadia Chen",
      amount: 249.95,
      currency: "USD",
      location: "Singapore",
      merchant: "Northwind Electronics",
      risk: "Critical",
      status: "review",
      action: "Review",
      riskScore: 82,
    },
    {
      id: "txn_1002",
      customer: "Ethan Brooks",
      amount: 18.4,
      currency: "USD",
      location: "London",
      merchant: "Harbor Coffee",
      risk: "High",
      status: "clear",
      action: "Investigate",
      riskScore: 65,
    },
    {
      id: "txn_1003",
      customer: "Ava Patel",
      amount: 1599.0,
      currency: "USD",
      location: "New York",
      merchant: "Orbit Mobility",
      risk: "Medium",
      status: "escalated",
      action: "Monitor",
      riskScore: 45,
    },
  ];

  const handleInvestigate = async (transaction: TransactionRow) => {
    setSelectedAlert(transaction.id);
    setSelectedTransaction(transaction);
    setIsLoading(true);
    setError(null);
    setInvestigation(null);
    setFeedbackSuccess(null);

    try {
      const result = await investigateTransaction({
        transaction_id: transaction.id,
        customer: transaction.customer,
        amount: transaction.amount,
        currency: transaction.currency,
        location: transaction.location,
        merchant: transaction.merchant,
        risk_score: transaction.riskScore,
      });
      setInvestigation(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Investigation failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (feedbackType: "confirm_fraud" | "false_positive" | "legitimate") => {
    if (!investigation || !selectedTransaction) return;

    setFeedbackSubmitting(true);
    setError(null);
    setFeedbackSuccess(null);

    try {
      // Create a temporary investigation ID for now
      const investigationId = `inv_${selectedTransaction.id}_${Date.now()}`;
      
      await submitAnalystFeedback({
        investigation_id: investigationId,
        transaction_id: selectedTransaction.id,
        amount: selectedTransaction.amount,
        location: selectedTransaction.location,
        merchant: selectedTransaction.merchant,
        original_risk_level: investigation.risk_level,
        original_confidence: investigation.confidence_score,
        feedback_type: feedbackType,
        analyst_notes: `Analyst feedback: ${feedbackType}`,
        actual_outcome: `Transaction determined to be ${feedbackType.replace("_", " ")}`
      });

      const feedbackMessages = {
        confirm_fraud: "Fraud confirmed - added to hindsight memory",
        false_positive: "False positive recorded - improves future detection",
        legitimate: "Marked as legitimate - learning memory updated"
      };

      setFeedbackSuccess(feedbackMessages[feedbackType]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit feedback");
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "critical":
        return "border-red-500/50 bg-red-500/10 text-red-100";
      case "high":
        return "border-orange-500/50 bg-orange-500/10 text-orange-100";
      case "medium":
        return "border-yellow-500/50 bg-yellow-500/10 text-yellow-100";
      case "low":
        return "border-green-500/50 bg-green-500/10 text-green-100";
      default:
        return "border-white/10 bg-white/5 text-white";
    }
  };

  return (
    <section className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr_0.8fr]">
      <div className="glass-card gradient-border p-5">
        <h3 className="text-lg font-semibold text-white">Transactions to Review</h3>
        <div className="mt-4 space-y-3">
          {mockTransactions.map((txn) => (
            <button
              key={txn.id}
              onClick={() => handleInvestigate(txn)}
              disabled={isLoading && selectedAlert === txn.id}
              className={`w-full rounded-2xl border p-4 text-left text-sm transition ${
                selectedAlert === txn.id
                  ? "border-cyan-400/50 bg-cyan-400/10"
                  : "border-white/10 bg-white/5 hover:bg-white/10"
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1">
                  <p className="text-xs uppercase tracking-[0.25em] text-cyan-200/70">{txn.id}</p>
                  <p className="mt-2 font-medium text-slate-100">{txn.customer}</p>
                  <p className="text-xs text-slate-400 mt-1">{txn.merchant}</p>
                </div>
                <span className={`rounded-full px-2 py-1 text-xs font-medium ${getRiskColor(txn.risk)}`}>
                  {txn.risk}
                </span>
              </div>
              {isLoading && selectedAlert === txn.id && (
                <div className="mt-3 flex items-center gap-2 text-cyan-300">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  <span className="text-xs">Investigating...</span>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      <div className="glass-card gradient-border p-5">
        <div className="flex items-center gap-3 border-b border-white/10 pb-4">
          <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-3 text-cyan-100">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">AI Investigation Report</h3>
            <p className="text-sm text-slate-400">Powered by Groq + Memory Search</p>
          </div>
        </div>

        {!investigation && !error && (
          <div className="mt-8 flex flex-col items-center justify-center gap-3 py-12">
            <BrainCircuit className="h-12 w-12 text-slate-600" />
            <p className="text-sm text-slate-400">Select a transaction to investigate</p>
          </div>
        )}

        {error && (
          <div className="mt-5 rounded-2xl border border-red-500/30 bg-red-500/10 p-4">
            <p className="text-sm text-red-100">{error}</p>
          </div>
        )}

        {investigation && (
          <div className="mt-5 space-y-4">
            <div className={`rounded-2xl border p-4 ${getRiskColor(investigation.risk_level)}`}>
              <p className="text-xs uppercase tracking-[0.25em] font-semibold">Risk Assessment</p>
              <div className="mt-3 flex items-baseline justify-between">
                <p className="text-3xl font-bold">{investigation.risk_level}</p>
                <p className="text-lg font-semibold opacity-75">{Math.round(investigation.confidence_score)}% confidence</p>
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Investigation Summary</p>
              <p className="mt-2 text-sm text-slate-200 leading-relaxed">{investigation.investigation_summary}</p>
            </div>

            <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-emerald-200">Recommended Action</p>
              <p className="mt-2 text-lg font-semibold text-emerald-100">{investigation.recommended_action}</p>
            </div>

            {investigation.fraud_indicators && investigation.fraud_indicators.length > 0 && (
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Fraud Indicators</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {investigation.fraud_indicators.map((indicator: string, idx: number) => (
                    <span key={idx} className="rounded-full border border-orange-500/30 bg-orange-500/10 px-3 py-1 text-xs text-orange-100">
                      {indicator}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {feedbackSuccess && (
              <div className="rounded-2xl border border-green-500/30 bg-green-500/10 p-4 flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-green-100">{feedbackSuccess}</p>
              </div>
            )}

            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-400 mb-3">Analyst Feedback - Help train the system</p>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => handleFeedback("confirm_fraud")}
                  disabled={feedbackSubmitting}
                  className="flex-1 min-w-[120px] flex items-center justify-center gap-2 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm font-medium text-red-100 hover:bg-red-500/20 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {feedbackSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ThumbsUp className="h-4 w-4" />}
                  Confirm Fraud
                </button>
                <button
                  onClick={() => handleFeedback("false_positive")}
                  disabled={feedbackSubmitting}
                  className="flex-1 min-w-[120px] flex items-center justify-center gap-2 rounded-lg border border-yellow-500/30 bg-yellow-500/10 px-3 py-2 text-sm font-medium text-yellow-100 hover:bg-yellow-500/20 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {feedbackSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <AlertTriangle className="h-4 w-4" />}
                  False Positive
                </button>
                <button
                  onClick={() => handleFeedback("legitimate")}
                  disabled={feedbackSubmitting}
                  className="flex-1 min-w-[120px] flex items-center justify-center gap-2 rounded-lg border border-green-500/30 bg-green-500/10 px-3 py-2 text-sm font-medium text-green-100 hover:bg-green-500/20 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {feedbackSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle className="h-4 w-4" />}
                  Legitimate
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="glass-card gradient-border p-5">
        <h3 className="text-lg font-semibold text-white">Alert Stream</h3>
        <div className="mt-4 space-y-3">
          <div className="rounded-2xl border border-red-400/20 bg-red-400/10 p-4">
            <div className="flex items-center gap-2 text-red-100">
              <AlertTriangle className="h-4 w-4" />
              Critical risk pattern
            </div>
            <p className="mt-2 text-sm text-red-50/80">Device reuse detected across three geography jumps within 19 minutes.</p>
          </div>
          <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
            <div className="flex items-center gap-2 text-cyan-100">
              <BrainCircuit className="h-4 w-4" />
              Memory reinforcement
            </div>
            <p className="mt-2 text-sm text-cyan-50/80">The model retrieved a similar case resolved on 2026-05-24.</p>
          </div>
          {alerts.slice(0, 1).map((alert) => (
            <div key={alert.type} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-slate-400">{alert.type}</p>
              <p className="mt-2 text-sm text-slate-200">{alert.message}</p>
              <p className="mt-2 text-xs text-slate-500">{alert.time}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
