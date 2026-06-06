# Memory Risk Intelligence Agent

A **fraud detection intelligence platform** combining AI-powered investigation with adaptive hindsight learning. The system uses Next.js frontend with a Python FastAPI backend, incorporating Groq's LLM for intelligent fraud analysis and XGBoost for risk scoring.

## 🎯 Key Features

### Fraud Investigation
- **AI-Powered Analysis** - Groq LLM analyzes transactions in context of historical fraud patterns
- **Risk Scoring** - Real-time transaction risk assessment with confidence metrics
- **Hindsight Learning** - Analyst feedback loops create self-improving fraud detection
- **Similar Case Discovery** - Finds past cases with matching patterns to inform current decisions

### Intelligence Platform
- **Knowledge Graph** - Visualizes relationships between customers, merchants, devices, and fraud cases
- **Memory Explorer** - Search and retrieve past investigations and learned patterns
- **Risk Heatmap** - Geographic visualization of fraud hotspots
- **Case Management** - Centralized workspace for fraud investigations
- **Live Monitoring** - Real-time transaction stream with risk indicators
- **Analytics Hub** - Fraud trends, analyst performance, and system insights

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 15)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes: Dashboard | AI Investigator | Knowledge     │   │
│  │  Graph | Memory | Analytics | Live Transactions      │   │
│  └────────────────────────┬─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                Backend (FastAPI + SQLAlchemy)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Core Endpoints:                                     │   │
│  │  • /investigate - Transaction analysis              │   │
│  │  • /feedback - Store analyst insights              │   │
│  │  • /hindsight/similar-cases - Pattern matching      │   │
│  │  • /dashboard, /transactions, /alerts, /memories    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services:                                           │   │
│  │  • Groq LLM Integration (fraud reasoning)           │   │
│  │  • XGBoost ML Models (risk scoring)                 │   │
│  │  • SQLAlchemy ORM (data layer)                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │   PostgreSQL Database                 │
         │  • Transactions                       │
         │  • Investigations                     │
         │  • Memory (learned patterns)          │
         │  • HindsightMemory (analyst feedback) │
         └───────────────────────────────────────┘
```

## 🗂️ Project Structure

```
├── app/                          # Next.js 15 app router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Dashboard
│   ├── ai-investigator/         # Fraud investigation UI
│   ├── knowledge-graph/         # Entity relationships
│   ├── memory-explorer/         # Search learned patterns
│   ├── live-transactions/       # Real-time feed
│   └── ...other routes
│
├── components/                   # React components
│   ├── graph/                   # Knowledge graph visualization
│   ├── charts/                  # Analytics & visualization
│   ├── dashboard/               # Dashboard components
│   ├── ai/                      # AI investigator UI
│   ├── case/                    # Case management
│   ├── memory/                  # Memory explorer
│   ├── live/                    # Live transactions
│   ├── profile/                 # User profile
│   ├── navigation/              # Navigation UI
│   └── ui/                      # Reusable UI primitives
│
├── lib/
│   ├── api.ts                  # Frontend API client
│   └── utils.ts                # Utility functions
│
├── backend/                      # Python FastAPI
│   ├── main.py                 # FastAPI app & endpoints
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── database.py             # DB connection & initialization
│   ├── models/                 # ML models
│   ├── requirements.txt        # Python dependencies
│   └── tests/                  # Backend tests
│
├── package.json                 # Frontend dependencies
├── tsconfig.json               # TypeScript config
├── next.config.mjs             # Next.js config
├── tailwind.config.ts          # Tailwind CSS config
└── .env.example                # Environment variables template
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- PostgreSQL 12+

### Installation

1. **Clone and navigate**
   ```bash
   cd AGENT
   ```

2. **Setup Frontend**
   ```bash
   npm install
   ```

3. **Setup Backend**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   cd backend && pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy examples
   cp .env.example .env.local
   cp backend/.env.example backend/.env
   
   # Edit with your values
   # .env.local: NEXT_PUBLIC_FASTAPI_BASE_URL
   # backend/.env: DATABASE_URL, GROQ_API_KEY
   ```

5. **Start Services**
   ```bash
   # Terminal 1: Backend
   cd backend && python -m uvicorn main:app --reload
   
   # Terminal 2: Frontend  
   npm run dev
   ```

6. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs (if enabled)

## 📊 Database Schema

### Transactions
Records financial transactions flagged for review.

### Investigations  
Fraud analysis tasks assigned to analysts.

### Memory
Learned fraud patterns and historical insights.

### HindsightMemory
Analyst feedback on investigation outcomes (NEW - for learning).

## 🔧 Configuration

### Environment Variables

**Frontend (.env.local)**
```
NEXT_PUBLIC_FASTAPI_BASE_URL=http://localhost:8000
```

**Backend (backend/.env)**
```
DATABASE_URL=postgresql://user:pass@localhost:5432/fraud_db
GROQ_API_KEY=your_groq_api_key
ENVIRONMENT=development
```

## 📡 API Endpoints

### Investigation
- `POST /investigate` - Analyze transaction for fraud risk
- `POST /feedback` - Store analyst feedback on investigation
- `GET /hindsight/similar-cases` - Find similar past cases

### Data
- `GET /dashboard` - Dashboard KPIs and metrics
- `GET /transactions` - Transaction list
- `GET /alerts` - Active fraud alerts
- `GET /memories` - Learned fraud patterns
- `POST /memory/search` - Search historical patterns
- `POST /memory/store` - Save new fraud pattern

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest test_main.py -v
pytest test_fraud_detection.py -v
pytest test_analyst_feedback.py -v

# Frontend linting
npm run lint
```

## 🛠️ Development

### Adding New Features

1. **Frontend** - Add route in `app/` or component in `components/`
2. **Backend** - Add endpoint in `backend/main.py` with schema validation
3. **Database** - Define model in `backend/models.py`, schema in `backend/schemas.py`

### Key Technologies

| Layer | Tech | Purpose |
|-------|------|---------|
| Frontend | Next.js 15, React 19 | UI framework |
| Styling | Tailwind CSS | Component styling |
| Visualization | Recharts, ReactFlow | Charts & graphs |
| Backend | FastAPI | REST API |
| Database | SQLAlchemy, PostgreSQL | Data persistence |
| AI | Groq API | LLM-powered analysis |
| ML | XGBoost | Risk scoring |

## 🚨 Troubleshooting

### Backend Connection Error
```
Check: NEXT_PUBLIC_FASTAPI_BASE_URL in .env.local matches backend URL
Run: Backend on same port (8000) or update frontend config
```

### Database Connection Error
```
Check: DATABASE_URL format in backend/.env
Check: PostgreSQL running and accessible
Run: psql -U user -h localhost -d fraud_db
```

### Missing GROQ_API_KEY
```
The system falls back to rule-based analysis without Groq
Get key from: https://console.groq.com/keys
Add to backend/.env to enable AI analysis
```

### Import Errors
```
Run: cd backend && pip install -r requirements.txt
Verify: All dependencies installed with correct versions
```

## 📈 Performance

- **Frontend**: Optimized React components, CSS-in-JS with Tailwind
- **Backend**: Async FastAPI, query optimization with SQLAlchemy
- **Database**: Indexed queries on transaction_id, investigation_id, created_at
- **Caching**: In-memory mock data when DB unavailable (graceful degradation)

## 🔐 Security Considerations

- [ ] Add API authentication (JWT tokens)
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Add CORS whitelist for production domains
- [ ] Encrypt sensitive database fields
- [ ] Implement audit logging for analyst actions

## 📝 License

[Add your license here]

## 🤝 Contributing

Contributions welcome! Please ensure:
1. Tests pass: `pytest` & `npm run lint`
2. Types are correct: `tsc --noEmit`
3. Documentation updated for new features

---

**Status**: ✅ All critical issues fixed | ✅ Endpoints implemented | ✅ Documentation complete
