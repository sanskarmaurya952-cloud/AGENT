# Architecture Diagram - Memory Risk Intelligence Agent

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                              │
│                            (Next.js 15, React 19)                           │
├────────────────┬──────────────────────────────────────────────────┬─────────┤
│   Dashboard    │  AI Investigator │ Knowledge Graph │  Analytics  │ Settings│
│  (KPIs, Stats) │  (Risk Analysis) │ (Entity Links)  │  (Trends)   │(Profile)│
│                │                  │                 │             │         │
│ • Real-time    │ • Transaction    │ • Customers     │ • Fraud     │ • Theme │
│   metrics      │   analysis       │ • Merchants     │   trends    │ • Prefs │
│ • Fraud trend  │ • Risk scoring   │ • Devices       │ • Analyst   │         │
│ • KPI cards    │ • Memory context │ • Locations     │   perf      │         │
│                │ • Feedback form  │ • Fraud cases   │ • Learning  │         │
└────────────────┴──────────────────────────────────────────────────┴─────────┘
                                    │ HTTP/REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          API GATEWAY LAYER                                  │
│                         (FastAPI, Port 8000)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ CORS Middleware │ Request Validation │ Error Handling │ Response Formatting │
└────────┬────────────────────────────────────────────────────────────────────┘
         │
         ├─────────────────────┬─────────────────────┬─────────────────────┐
         ▼                     ▼                     ▼                     ▼
    ┌─────────┐          ┌──────────┐          ┌──────────┐          ┌──────────┐
    │ Endpoint│          │ Endpoint │          │ Endpoint │          │ Endpoint │
    │ Layer   │          │ Layer    │          │ Layer    │          │ Layer    │
    │ (Routes)│          │ (Routes) │          │ (Routes) │          │ (Routes) │
    └────┬────┘          └────┬─────┘          └────┬─────┘          └────┬─────┘
         │ POST /investigate  │ POST /feedback     │ GET /hindsight    │ GET /dashboard
         │                    │ GET /memories      │ /similar-cases    │ GET /transactions
         │                    │ POST /memory/search│                   │ GET /alerts
         │                    │ POST /memory/store │                   │
         └────────────────────┴──────────────────┬─────────────────────┘
                                                │
        ┌───────────────────────────────────────┴────────────────────┐
        ▼                                                             ▼
┌──────────────────────┐                                   ┌────────────────────┐
│  SERVICE LAYER       │                                   │  DATA ACCESS LAYER │
│  (Business Logic)    │                                   │  (SQLAlchemy ORM)  │
├──────────────────────┤                                   ├────────────────────┤
│                      │                                   │                    │
│ • Groq LLM Client    │◄─────────────────────────────────►│  Transaction Model │
│ • XGBoost ML Model   │                                   │  Investigation     │
│ • Pattern Matching   │                                   │  Memory            │
│ • Analysis Engine    │                                   │  HindsightMemory   │
│                      │                                   │                    │
└──────────────────────┘                                   └────────┬───────────┘
         │                                                          │
         ├──────────────────────┐                                  │
         ▼                      ▼                                  ▼
    ┌─────────────┐         ┌──────────┐              ┌─────────────────────┐
    │ Groq API    │         │ ML Models│              │   PostgreSQL DB     │
    │ (LLM)       │         │ (models/)│              │   (Data Storage)    │
    │             │         │          │              │                     │
    │ • Analyze   │         │ • Fraud  │              │ Tables:             │
    │   fraud     │         │   XGBoost│              │ - transactions      │
    │ • Score     │         │ • Risk   │              │ - investigations    │
    │   risk      │         │   scoring│              │ - memories          │
    │ • Generate  │         │          │              │ - hindsight_memories│
    │   reasoning │         │          │              │                     │
    └─────────────┘         └──────────┘              └─────────────────────┘
              │                                              │
              └──────────────────┬──────────────────────────┘
                                 ▼
              ┌──────────────────────────────────┐
              │  External Services/Integrations  │
              ├──────────────────────────────────┤
              │ • Groq API (LLM Inference)      │
              │ • ML Model Files (.model)        │
              │ • Authentication (future JWT)    │
              └──────────────────────────────────┘
```

## Data Flow Diagrams

### Fraud Investigation Flow

```
User Transaction Input
        │
        ▼
    ┌─────────────────────────────────┐
    │ POST /investigate               │
    │ (InvestigateTransactionRequest) │
    └─────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────────────┐
        │ Search Similar Memories                │
        │ (query: merchant + location + customer)│
        └─────────────┬───────────────────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Found Similar Cases ────►│ Add to context
          │ (3 past fraud patterns) │
          └────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │ Call Groq LLM API (or rules)   │
        │ - Transaction summary           │
        │ - Related fraud memories        │
        │ - Past analyst decisions        │
        └─────────────┬───────────────────┘
                      │
                      ▼
          ┌─────────────────────────────┐
          │ LLM generates analysis:     │
          │ • Risk Level                │
          │ • Fraud Type                │
          │ • Confidence Score          │
          │ • Reasoning                 │
          │ • Recommended Action        │
          └─────────────┬───────────────┘
                        │
                        ▼
              ┌────────────────────────┐
              │ Store Investigation   │
              │ Create Investigation  │
              │ Record               │
              └────────────┬──────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │ Return Report    │
                    │ (InvestigationRep│
                    │ort)             │
                    └──────────────────┘
                           │
                           ▼
                    User Reviews Report
```

### Hindsight Learning Flow

```
Analyst Reviews Investigation
        │
        ▼
    ┌───────────────────────────────────┐
    │ Analyst Submits Feedback          │
    │ (Was it fraud? Decision correct?) │
    └─────────────┬─────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │ POST /feedback                  │
        │ (AnalystFeedbackRequest)        │
        │ - investigation_id              │
        │ - feedback_type (confirm/false) │
        │ - analyst_notes                 │
        │ - actual_outcome                │
        └─────────────┬───────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │ Store HindsightMemory           │
        │ (New: analyst feedback record)  │
        └─────────────┬───────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │ Update Model Accuracy Metrics   │
        │ • Track correct predictions     │
        │ • Track false positives         │
        │ • Build confidence curves       │
        └─────────────┬───────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │ Next Investigation Uses Data    │
        │ Similar patterns reference      │
        │ this feedback via GET           │
        │ /hindsight/similar-cases        │
        └─────────────────────────────────┘
```

### Similar Cases Lookup Flow

```
During Investigation Analysis
        │
        ▼
    ┌───────────────────────────┐
    │ GET /hindsight/           │
    │ similar-cases             │
    │ ?amount=1000              │
    │ &location=NYC             │
    │ &merchant=Vendor          │
    │ &limit=5                  │
    └─────────────┬─────────────┘
                  │
                  ▼
        ┌─────────────────────────────┐
        │ Query HindsightMemory Table │
        │ Match on:                   │
        │ - location = NYC            │
        │ - merchant ~ Vendor         │
        │ Recent records only         │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌──────────────────────────────────┐
        │ Found 3 Similar Cases:           │
        │ • Case A: $1200 → fraud confirm  │
        │ • Case B: $890 → false positive  │
        │ • Case C: $1150 → fraud confirm  │
        └─────────────┬────────────────────┘
                      │
                      ▼
        ┌──────────────────────────────────┐
        │ Calculate Accuracy Rate:         │
        │ 2 correct / 3 total = 66.7%     │
        └─────────────┬────────────────────┘
                      │
                      ▼
        ┌──────────────────────────────────┐
        │ Return SimilarCasesContext       │
        │ • Similar cases list             │
        │ • Accuracy rate                  │
        │ • Common patterns found          │
        └──────────────────────────────────┘
```

## Component Hierarchy

```
<KnowledgeGraph>
├── <IntelligenceNode>
│   ├── Handle (target, source)
│   └── Styling (cyan-400)
└── Sidebar
    ├── Node Details
    │   └── Connection info
    └── Relationship trace

<AiInvestigator>
├── Transaction Input
│   ├── Customer field
│   ├── Amount field
│   └── Submit button
├── Analysis Result
│   ├── Risk Level
│   ├── Fraud Type
│   └── Confidence
└── Feedback Form
    ├── Feedback type selector
    ├── Analyst notes
    └── Submit button

<DashboardShell>
├── <Topbar>
│   ├── Title
│   └── ThemeToggle
├── <Sidebar>
│   ├── Navigation
│   ├── Logo
│   └── User Profile
└── <MainContent>
    ├── Page content
    └── Footer
```

## Database Schema

```sql
-- Transactions: Financial transactions
CREATE TABLE transactions (
  id VARCHAR(36) PRIMARY KEY,
  customer VARCHAR(255),
  amount FLOAT,
  location VARCHAR(255),
  merchant VARCHAR(255),
  risk_score INT,
  created_at TIMESTAMP,
  -- Relationships: investigations (1:many)
);

-- Investigations: Fraud analysis records
CREATE TABLE investigations (
  id VARCHAR(36) PRIMARY KEY,
  transaction_id VARCHAR(36) FK,
  status VARCHAR(50),
  severity VARCHAR(50),
  created_at TIMESTAMP,
  -- Relationships: memories (1:many), hindsight_memories (1:many)
);

-- Memories: Learned fraud patterns
CREATE TABLE memories (
  id VARCHAR(36) PRIMARY KEY,
  investigation_id VARCHAR(36) FK,
  title VARCHAR(255),
  fraud_type VARCHAR(100),
  risk_level VARCHAR(50),
  confidence FLOAT,
  created_at TIMESTAMP
);

-- HindsightMemories: Analyst feedback (NEW)
CREATE TABLE hindsight_memories (
  id VARCHAR(36) PRIMARY KEY,
  investigation_id VARCHAR(36) FK,
  transaction_id VARCHAR(36),
  feedback_type VARCHAR(50), -- confirm_fraud, false_positive, legitimate
  original_risk_level VARCHAR(50),
  analyst_notes TEXT,
  actual_outcome VARCHAR(100),
  created_at TIMESTAMP,
  -- Used by: /hindsight/similar-cases endpoint
);
```

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (npm run dev) → port 3000
├── Backend (uvicorn) → port 8000
└── PostgreSQL (local) → port 5432
```

### Production
```
Load Balancer
├── Frontend (Vercel/AWS S3+CloudFront)
├── Backend Cluster (AWS ECS/EKS)
│   ├── API Container 1 (FastAPI)
│   ├── API Container 2 (FastAPI)
│   └── API Container 3 (FastAPI)
├── Database (RDS PostgreSQL)
├── Cache (Redis)
└── Monitoring (CloudWatch)
```

## Key Integration Points

| Component | Integrated With | Purpose |
|-----------|-----------------|---------|
| Groq API | Backend Service | LLM-powered fraud analysis |
| XGBoost | Backend ML | Risk scoring |
| SQLAlchemy | Database | Data persistence |
| React Flow | Frontend | Knowledge graph visualization |
| Tailwind CSS | Frontend | Component styling |
| Next.js | Frontend | Page routing & SSR |

---

**Status**: ✅ Architecture documented | All systems integrated
