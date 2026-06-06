const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function getApiBaseUrl() {
  return process.env.FASTAPI_BASE_URL ?? process.env.NEXT_PUBLIC_FASTAPI_BASE_URL ?? DEFAULT_API_BASE_URL;
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export type DashboardKpi = {
  label: string;
  value: string;
  delta: string;
  tone: string;
};

export type DashboardMemoryCard = {
  title: string;
  riskLevel: string;
  fraudType: string;
  confidence: number;
  date: string;
  learningImpact: string;
};

export type DashboardResponse = {
  kpis: DashboardKpi[];
  summary: {
    totalTransactions: number;
    flaggedTransactions: number;
    highRiskAlerts: number;
    analystQueue: number;
  };
  trend: Array<{ date: string; transactions: number; flags: number }>;
  topInsights: string[];
  memoryCards: DashboardMemoryCard[];
};

export type TransactionRow = {
  id: string;
  customer: string;
  amount: number;
  currency: string;
  location: string;
  merchant: string;
  risk: string;
  status: string;
  action: string;
  riskScore: number;
};

export type TransactionsResponse = {
  items: TransactionRow[];
  page: number;
  pageSize: number;
  total: number;
};

export type AlertItem = {
  id: string;
  type: string;
  severity: string;
  message: string;
  status: string;
  time: string;
};

export type AlertsResponse = {
  items: AlertItem[];
};

export type MemoryStoreRequest = {
  investigation_id?: string | null;
  title: string;
  content: string;
  risk_level: string;
  fraud_type: string;
  confidence: number;
  learning_impact?: string | null;
};

export type MemoryItem = {
  id: string;
  investigationId: string | null;
  title: string;
  content: string;
  riskLevel: string;
  fraudType: string;
  confidence: number;
  learningImpact: string;
  createdAt: string;
};

export type MemorySearchResponse = {
  query: string;
  count: number;
  items: MemoryItem[];
};

export type MemoriesResponse = {
  items: MemoryItem[];
  total: number;
};

export async function getDashboardData() {
  return fetchJson<DashboardResponse>("/dashboard");
}

export async function getTransactionsData() {
  return fetchJson<TransactionsResponse>("/transactions");
}

export async function getAlertsData() {
  return fetchJson<AlertsResponse>("/alerts");
}

export async function getMemories(limit = 25) {
  return fetchJson<MemoriesResponse>("/memories", {
    method: "GET",
  });
}

export async function storeMemory(payload: MemoryStoreRequest) {
  return fetchJson<{ memory: MemoryItem }>("/memory/store", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function searchMemory(query: string, limit = 5) {
  return fetchJson<MemorySearchResponse>("/memory/search", {
    method: "POST",
    body: JSON.stringify({ query, limit }),
  });
}

export type InvestigateTransactionRequest = {
  transaction_id: string;
  customer: string;
  amount: number;
  currency: string;
  location: string;
  merchant: string;
  risk_score: number;
};

export type InvestigationReport = {
  transaction_id: string;
  risk_level: string;
  confidence: number;
  fraud_type: string;
  reasoning: string;
  related_memories: number;
  recommended_action: string;
  investigation_notes: string;
};

export async function investigateTransaction(payload: InvestigateTransactionRequest) {
  return fetchJson<InvestigationReport>("/investigate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export type AnalystFeedbackRequest = {
  investigation_id: string;
  transaction_id: string;
  amount: number;
  location: string;
  merchant: string;
  original_risk_level: string;
  original_confidence: number;
  feedback_type: "confirm_fraud" | "false_positive" | "legitimate";
  analyst_notes?: string;
  actual_outcome?: string;
};

export type HindsightMemoryResponse = {
  memory_id: string;
  feedback_type: string;
  message: string;
};

export type SimilarCase = {
  amount: number;
  location: string;
  merchant: string;
  original_risk: string;
  feedback: string;
  outcome: string;
  date: string;
};

export type SimilarCasesContext = {
  similar_cases: SimilarCase[];
  accuracy_rate: number;
  common_patterns: string[];
};

export async function submitAnalystFeedback(payload: AnalystFeedbackRequest) {
  return fetchJson<HindsightMemoryResponse>("/feedback", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getSimilarCases(amount: number, location: string, merchant: string, limit = 5) {
  const params = new URLSearchParams({
    amount: amount.toString(),
    location,
    merchant,
    limit: limit.toString(),
  });
  return fetchJson<SimilarCasesContext>(`/hindsight/similar-cases?${params}`, {
    method: "GET",
  });
}