# Setup Guide - Memory Risk Intelligence Agent

Complete step-by-step guide to get the fraud detection platform running locally or in production.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB for dependencies

### Required Software
- **Node.js**: v18+ (https://nodejs.org)
- **Python**: 3.11+ (https://www.python.org)
- **PostgreSQL**: 12+ (https://www.postgresql.org)
- **Git** (optional but recommended)

### Third-party Accounts
- **Groq API Key** (free tier available): https://console.groq.com

## 🖥️ Local Development Setup

### Step 1: Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd AGENT

# Or manually download and extract
cd path/to/AGENT
```

### Step 2: Install Node Dependencies

```bash
npm install
```

This installs all frontend dependencies including:
- Next.js 15.4.4
- React 19
- Tailwind CSS
- Recharts (charts)
- ReactFlow (knowledge graph)
- Framer Motion (animations)

**Expected output**: "added X packages in Ys"

### Step 3: Setup Python Backend

#### Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key packages installed**:
- fastapi>=0.115 - REST API framework
- sqlalchemy>=2.0 - ORM
- psycopg[binary]>=3.2 - PostgreSQL driver
- groq>=0.4 - Groq LLM client
- python-dotenv>=1.0 - Environment variables
- xgboost>=2.0 - ML model
- pandas>=2.0 - Data processing
- pytest>=7.0 - Testing

### Step 4: Setup PostgreSQL Database

#### Option A: Local PostgreSQL

```bash
# Create database
psql -U postgres
CREATE DATABASE fraud_detection_agent;
CREATE USER fraud_agent WITH PASSWORD 'secure_password';
ALTER ROLE fraud_agent SET client_encoding TO 'utf8';
ALTER ROLE fraud_agent SET default_transaction_isolation TO 'read committed';
ALTER ROLE fraud_agent SET default_transaction_deferrable TO on;
ALTER ROLE fraud_agent SET default_transaction_readonly TO off;
GRANT ALL PRIVILEGES ON DATABASE fraud_detection_agent TO fraud_agent;
\q
```

#### Option B: Docker PostgreSQL

```bash
docker run --name fraud_db \
  -e POSTGRES_USER=fraud_agent \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=fraud_detection_agent \
  -p 5432:5432 \
  -d postgres:15
```

#### Option C: Skip (Use Mock Data)

The backend gracefully falls back to in-memory mock data if no database is available.

### Step 5: Configure Environment Variables

#### Frontend Configuration

Create `.env.local` in project root:

```bash
# .env.local
NEXT_PUBLIC_FASTAPI_BASE_URL=http://localhost:8000
```

#### Backend Configuration

Create `backend/.env`:

```bash
# backend/.env

# Database (REQUIRED for persistence)
DATABASE_URL=postgresql://fraud_agent:secure_password@localhost:5432/fraud_detection_agent

# Groq API (Optional - system works without it with rule-based analysis)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Environment
ENVIRONMENT=development
DEBUG=true
```

**Get GROQ_API_KEY**:
1. Go to https://console.groq.com
2. Sign up/login
3. Create API key
4. Paste in backend/.env

### Step 6: Initialize Database

```bash
cd backend
python -c "from database import init_db; init_db()"
```

This creates tables:
- `transactions`
- `investigations`
- `memories`
- `hindsight_memories`

And seeds sample data.

### Step 7: Verify Backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Test endpoints**:
```bash
# In another terminal
curl http://localhost:8000/dashboard
curl http://localhost:8000/transactions
```

### Step 8: Start Frontend

```bash
# From project root (exit backend terminal or use new terminal)
npm run dev
```

**Expected output**:
```
▲ Next.js 15.4.4
  - Local:        http://localhost:3000
  - Environments: .env.local
✓ Ready in 2.1s
```

### Step 9: Access Application

Open browser to: http://localhost:3000

**Default Features Available**:
- ✅ Dashboard with KPIs
- ✅ AI Investigator (Groq LLM analysis)
- ✅ Knowledge Graph (entity relationships)
- ✅ Memory Explorer (pattern search)
- ✅ Live Transactions (real-time feed)
- ✅ Risk Heatmap (geographic visualization)
- ✅ Case Management
- ✅ Analytics Hub

## 🧪 Verify Installation

### Backend Health Check

```bash
cd backend
python -c "
import main
import database
from sqlalchemy import text

with database.SessionLocal() as db:
    result = db.execute(text('SELECT COUNT(*) FROM transactions'))
    count = result.scalar()
    print(f'✓ Database connected: {count} transactions')
"
```

### Test API Endpoints

```bash
# Test investigation endpoint
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_123",
    "customer": "Test Customer",
    "amount": 1000,
    "currency": "USD",
    "location": "New York",
    "merchant": "Test Merchant",
    "risk_score": 75
  }'

# Test feedback endpoint
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "investigation_id": "inv_123",
    "transaction_id": "txn_123",
    "amount": 1000,
    "location": "New York",
    "merchant": "Test Merchant",
    "original_risk_level": "High",
    "original_confidence": 0.85,
    "feedback_type": "confirm_fraud",
    "analyst_notes": "Transaction was fraudulent"
  }'
```

### Run Tests

```bash
cd backend
pytest test_main.py -v
pytest test_analyst_feedback.py -v
```

## 🐳 Docker Setup (Optional)

### Build Docker Image

```bash
# Build
docker build -t fraud-agent:latest .

# Run
docker run -p 3000:3000 -p 8000:8000 \
  -e DATABASE_URL=postgresql://fraud_agent:pwd@postgres:5432/fraud_db \
  -e GROQ_API_KEY=your_key \
  fraud-agent:latest
```

## 🚀 Production Deployment

### Environment Setup

Update `backend/.env` and `.env.local`:

```bash
# backend/.env (Production)
DATABASE_URL=postgresql://prod_user:prod_password@prod_host:5432/fraud_db
GROQ_API_KEY=prod_groq_key
ENVIRONMENT=production
DEBUG=false

# .env.local (Production Frontend)
NEXT_PUBLIC_FASTAPI_BASE_URL=https://api.yourdomain.com
```

### Build for Production

```bash
# Frontend
npm run build
npm run start

# Backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Backups

```bash
# Backup
pg_dump -U fraud_agent fraud_detection_agent > backup.sql

# Restore
psql -U fraud_agent fraud_detection_agent < backup.sql
```

## 🔧 Troubleshooting

### Issue: "Cannot find module 'next'"

**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Database connection refused"

**Solution**:
```bash
# Check PostgreSQL running
psql -U postgres

# Check connection string
# Format: postgresql://user:password@host:port/database

# Verify database exists
psql -U fraud_agent -h localhost -d fraud_detection_agent
```

### Issue: "Groq API key invalid"

**Solution**:
```bash
# Verify key format
# Should start with: gsk_

# Get new key from https://console.groq.com/keys
# Update backend/.env and restart backend
```

### Issue: "Port 3000/8000 already in use"

**Solution**:
```bash
# Change port
npm run dev -- --port 3001
python -m uvicorn main:app --port 8001
```

### Issue: "Module not found: reactflow"

**Solution**:
```bash
npm install reactflow
```

## 📚 Next Steps

1. **Explore Features** - Visit each page in the UI
2. **Run Demo Script** - See `DEMO_SCRIPT.md` for walkthroughs
3. **Check Tests** - Run `pytest backend/` to verify
4. **Review Code** - Start in `backend/main.py` and `app/dashboard/page.tsx`
5. **Integrate Data** - Replace mock data with real transaction feeds

## 🆘 Getting Help

1. **Logs** - Check terminal output and backend logs
2. **Errors** - Read error messages carefully, check for typos
3. **Documentation** - See README.md and architecture docs
4. **Tests** - Review test files to understand expected behavior

---

**Status**: ✅ Setup complete | Ready to use!
