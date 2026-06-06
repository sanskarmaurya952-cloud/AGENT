# Demo Script - Memory Risk Intelligence Agent

Complete walkthrough demonstrating all key features of the fraud detection platform.

## 🎬 Demo Prerequisites

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ PostgreSQL database populated with sample data
- ✅ Optional: Groq API key configured (for AI analysis)

**Setup**: Follow SETUP_GUIDE.md before starting demo

---

## Demo 1: Dashboard Overview (5 min)

### Objective
Show real-time fraud metrics and system status.

### Steps

1. **Open Dashboard**
   ```
   URL: http://localhost:3000
   ```

2. **Point Out KPI Cards** (top section)
   - Total Transactions: 1,230
   - Flagged Transactions: 45
   - High Risk Alerts: 12
   - Analyst Queue: 8

3. **Show Fraud Trend Chart** (main area)
   - Displays last 30 days of transaction volume
   - Red line shows flagged/suspicious transactions
   - **Talking Point**: "Real-time tracking of fraud trends"

4. **Review Top Insights Section**
   - "3 synthetic identity clusters detected"
   - "Velocity spike from New York location"
   - "New merchant abuse pattern emerging"
   - **Talking Point**: "System automatically identifies emerging patterns"

5. **Highlight Memory Cards** (bottom section)
   - Each card shows a learned fraud pattern
   - Risk level, confidence, and impact
   - **Talking Point**: "These patterns improve prediction accuracy over time"

### Key Takeaway
The dashboard provides at-a-glance visibility into fraud activity and system learning progress.

---

## Demo 2: Fraud Investigation (10 min)

### Objective
Show AI-powered transaction analysis workflow.

### Steps

1. **Navigate to AI Investigator**
   ```
   Click: "AI Investigator" in left sidebar
   URL: http://localhost:3000/ai-investigator
   ```

2. **Enter Test Transaction**
   ```
   Customer: "Nadia Chen"
   Amount: $2,499.95
   Currency: USD
   Location: "Singapore"
   Merchant: "Electronics Retailer Pro"
   Risk Score: 82
   ```

3. **Click "Analyze Transaction"**
   - System calls `/investigate` endpoint
   - Backend searches for similar past cases
   - Groq LLM analyzes transaction
   - Takes ~3-5 seconds (longer with Groq)

4. **Review Investigation Report**
   - **Risk Level**: Critical ⚠️
   - **Fraud Type**: Synthetic Identity Fraud
   - **Confidence**: 96%
   - **Reasoning**: "High-value purchase from new device in unusual location..."
   - **Recommended Action**: Review
   - **Related Memories**: 3 similar past cases

   **Talking Points**:
   - "AI combines rule-based analysis with learned patterns"
   - "Groq LLM provides human-like reasoning"
   - "System references similar past cases"
   - "High confidence increases analyst trust"

5. **Show Investigation Notes Section**
   - Lists detected fraud indicators
   - Matches with historical patterns
   - Analyst can see why system flagged this

### User Actions

Show how analysts interact with results:

1. **Provide Analyst Feedback** (NEW endpoint)
   ```
   Radio: Select "Confirm Fraud"
   Notes: "Victim called - transaction unauthorized"
   Click: "Submit Feedback"
   ```

2. **System Response**
   ```
   Status: "Feedback recorded successfully"
   Message: "This will improve future fraud detection"
   ```

   **Talking Point**: "Analyst feedback trains the system for better future predictions"

### Key Takeaway
The investigation workflow combines AI analysis with analyst feedback for continuous improvement.

---

## Demo 3: Knowledge Graph (8 min)

### Objective
Show relationship visualization between fraud entities.

### Steps

1. **Navigate to Knowledge Graph**
   ```
   Click: "Knowledge Graph" in sidebar
   URL: http://localhost:3000/knowledge-graph
   ```

2. **Explore Graph**
   - Center: Transaction A (selected by default)
   - Connected nodes:
     - Customer: "Nadia Chen"
     - Device: "X9" (iPhone 14)
     - Merchant: "Northwind Electronics"
     - Location: "Singapore"
     - Fraud Case: "447"

3. **Click on Nodes** to change selection
   - Click on "Customer A" to see relationships
   - Click on "Merchant Nova" to see their patterns
   - Notice animated edges showing data flow

4. **Review Node Details Panel** (right side)
   - Selected Entity display
   - Connection Confidence: 97%
   - Risk Propagation: High
   - Memory Cluster: MX-447

   **Talking Point**: "High confidence connections help identify fraud rings and organized schemes"

5. **Zoom and Pan** (using controls)
   - Use mouse wheel to zoom
   - Drag to pan
   - Click Controls buttons
   - Use MiniMap (bottom right)

### Key Takeaway
Visual relationship analysis helps identify fraud networks and organized schemes.

---

## Demo 4: Memory Explorer (7 min)

### Objective
Show how learned fraud patterns are stored and searched.

### Steps

1. **Navigate to Memory Explorer**
   ```
   Click: "Memory Explorer" in sidebar
   URL: http://localhost:3000/memory-explorer
   ```

2. **Search for Fraud Patterns**
   ```
   Search Box: Type "synthetic identity"
   Click: Search button
   ```

3. **Review Search Results**
   - Result 1: "Synthetic identity ring"
     - Risk Level: Critical
     - Confidence: 96%
     - Found: 2024-05-20
   
   - Result 2: "Identity fraud detection improvements"
     - Risk Level: High
     - Confidence: 89%

4. **Click on a Memory Card** to expand details
   - Full content of fraud pattern
   - Related investigations
   - Analyst who discovered it
   - Learning impact: "+18% detection lift"

   **Talking Point**: "Each pattern represents months of analyst expertise captured systematically"

5. **Try Different Searches**
   - Search: "merchant" → finds merchant fraud patterns
   - Search: "velocity" → finds transaction velocity patterns
   - Search: "location" → finds geographic patterns

### Key Takeaway
Institutional memory grows with each investigation, making future detection more accurate.

---

## Demo 5: Similar Cases Lookup (NEW) (5 min)

### Objective
Show how the system finds historical context for new investigations.

### Steps

1. **In AI Investigator**, note the **Similar Cases** section
   - Shows past transactions with matching characteristics
   - Each case includes analyst feedback outcome

2. **Examine Similar Cases**
   ```
   Case 1:
   - Amount: $2,300 (similar to current $2,500)
   - Location: Singapore (same)
   - Merchant: "Electronics" (similar category)
   - Original Risk: High
   - Analyst Feedback: "Confirm Fraud"
   - Outcome: "Refunded, account secured"
   
   Case 2:
   - Amount: $1,900
   - Location: Singapore
   - Merchant: "Retail Electronics"
   - Original Risk: Medium
   - Analyst Feedback: "Confirm Fraud"
   - Outcome: "Investigation ongoing"
   ```

3. **Calculate Accuracy**
   ```
   Accuracy Rate: 89.5%
   Common Patterns:
   - Velocity spike from new device
   - Geographic mismatch
   - Merchant category change
   ```

   **Talking Point**: "89.5% accuracy on similar cases gives analysts high confidence in current assessment"

4. **Show Live Endpoint** (technical audience)
   ```bash
   curl "http://localhost:8000/hindsight/similar-cases?amount=2499.95&location=Singapore&merchant=Electronics&limit=5"
   ```

### Key Takeaway
Historical context helps analysts make informed decisions backed by proven outcomes.

---

## Demo 6: Live Transactions (5 min)

### Objective
Show real-time transaction feed.

### Steps

1. **Navigate to Live Transactions**
   ```
   Click: "Live Transactions" in sidebar
   URL: http://localhost:3000/live-transactions
   ```

2. **Examine Transaction Table**
   - Columns: Customer, Amount, Location, Merchant, Risk, Status, Action
   - Color coding by risk level:
     - 🔴 Red = Critical (Nadia Chen, $2,499.95)
     - 🟠 Orange = High (Ethan Brooks, $18.40)
     - 🟡 Yellow = Medium (Ava Patel, $1,599.00)

3. **Click on a Transaction Row**
   - Expands to show full details
   - Action buttons: "Investigate", "Clear", "Escalate"

4. **Click "Investigate" Button**
   - Routes to AI Investigator with transaction pre-loaded
   - Ready for immediate analysis

### Key Takeaway
Easy access to flagged transactions for quick analyst action.

---

## Demo 7: Risk Heatmap (5 min)

### Objective
Show geographic fraud distribution.

### Steps

1. **Navigate to Risk Heatmap**
   ```
   Click: "Risk Heatmap" in sidebar
   URL: http://localhost:3000/risk-heatmap
   ```

2. **Examine World Map**
   - Color intensity shows fraud risk by region
   - Red zones: High fraud activity
   - Blue zones: Low fraud activity

3. **Point Out Key Regions**
   - Singapore: Synthetic ID cluster
   - London: Merchant abuse patterns
   - New York: Geographic anomalies

4. **Click on Regions** to see details
   - Shows transactions from that region
   - Breakdown by fraud type
   - Recommended actions

### Key Takeaway
Geographic patterns help identify regional fraud schemes.

---

## Demo 8: Analytics Hub (5 min)

### Objective
Show system performance and analyst metrics.

### Steps

1. **Navigate to Analytics**
   ```
   Click: "Analytics" in sidebar
   URL: http://localhost:3000/analytics
   ```

2. **Review Fraud Breakdown** (Pie Chart)
   - Synthetic Identity: 45%
   - Merchant Abuse: 30%
   - Money Laundering: 15%
   - Card Fraud: 10%

3. **Show Fraud Trend** (Line Chart)
   - Transactions over 30 days
   - Flagged transactions overlay
   - Trend indicators

4. **Examine Analyst Decisions** (Bar Chart)
   - Each analyst's fraud catch rate
   - False positive rate
   - Average review time

5. **Review Memory Growth** (Area Chart)
   - New fraud patterns discovered
   - Learning velocity
   - System improvement trajectory

### Key Takeaway
Analytics show system effectiveness and identify training opportunities.

---

## Demo 9: Case Management (5 min)

### Objective
Show investigator collaboration workspace.

### Steps

1. **Navigate to Case Management**
   ```
   Click: "Case Management" in sidebar
   URL: http://localhost:3000/case-management
   ```

2. **View Case Board**
   - Status columns: Open, Investigating, Closed, Escalated
   - Drag-drop to change status
   - Color-coded by priority

3. **Click on a Case Card**
   - Shows full case details
   - Investigation timeline
   - Analyst notes
   - Related transactions

4. **Add Analyst Note**
   - Click "Add Note" button
   - Type investigation findings
   - Auto-saves to database

### Key Takeaway
Collaborative workspace for team-based fraud investigations.

---

## Demo 10: Settings & Profile (3 min)

### Objective
Show personalization features.

### Steps

1. **Navigate to Settings**
   ```
   Click: Gear icon (top right)
   URL: http://localhost:3000/settings
   ```

2. **Show Theme Toggle**
   - Toggle between Light/Dark mode
   - Preference saved locally

3. **Show Profile Settings**
   - User name display
   - Role/department
   - API key management (future)

### Key Takeaway
System personalizes for analyst preferences.

---

## Backend API Demo (Technical Audience) (10 min)

### Demonstrate API Endpoints

#### 1. Dashboard Endpoint
```bash
curl http://localhost:8000/dashboard
```
Returns: KPIs, summary stats, trends, insights, memory cards

#### 2. Transactions Endpoint
```bash
curl http://localhost:8000/transactions
```
Returns: Paginated transaction list

#### 3. Investigate Endpoint (Core Feature)
```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_123",
    "customer": "John Doe",
    "amount": 5000,
    "currency": "USD",
    "location": "New York",
    "merchant": "Electronics Store",
    "risk_score": 85
  }'
```
Returns: `InvestigationReport` with risk level, fraud type, confidence, reasoning

#### 4. Feedback Endpoint (NEW)
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "investigation_id": "inv_123",
    "transaction_id": "txn_123",
    "amount": 5000,
    "location": "New York",
    "merchant": "Electronics Store",
    "original_risk_level": "High",
    "original_confidence": 0.85,
    "feedback_type": "confirm_fraud",
    "analyst_notes": "Customer confirmed unauthorized"
  }'
```
Returns: `HindsightMemoryResponse` with confirmation

#### 5. Similar Cases Endpoint (NEW)
```bash
curl "http://localhost:8000/hindsight/similar-cases?amount=5000&location=New%20York&merchant=Electronics&limit=5"
```
Returns: `SimilarCasesContext` with similar past cases and accuracy metrics

#### 6. Memory Search Endpoint
```bash
curl -X POST http://localhost:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "synthetic identity", "limit": 5}'
```
Returns: Memory search results

### Key Points
- All endpoints validate input with Pydantic schemas
- Fallback to mock data if database unavailable
- Graceful error handling
- CORS enabled for frontend access

---

## Database Demo (Technical Audience) (5 min)

### Show Database Schema

```sql
-- View all tables
\dt

-- Count transactions
SELECT COUNT(*) FROM transactions;

-- View recent investigations
SELECT id, status, severity, created_at 
FROM investigations 
ORDER BY created_at DESC 
LIMIT 5;

-- View hindsight feedback (NEW)
SELECT feedback_type, COUNT(*) as count
FROM hindsight_memories
GROUP BY feedback_type;

-- Calculate accuracy
SELECT 
  feedback_type,
  COUNT(*) as count,
  ROUND(COUNT(*)::numeric / (SELECT COUNT(*) FROM hindsight_memories) * 100, 2) as percentage
FROM hindsight_memories
GROUP BY feedback_type;
```

### Key Points
- Clean schema design with proper relationships
- Cascade deletes for referential integrity
- Timestamps for audit trail
- Index on frequently queried fields

---

## 🎯 Demo Summary Talking Points

| Feature | Business Value | Technical Excellence |
|---------|-----------------|----------------------|
| **Dashboard** | Real-time fraud visibility | Efficient KPI calculation |
| **AI Investigation** | Faster analyst decisions | LLM + Rule-based hybrid |
| **Knowledge Graph** | Identify fraud rings | Graph visualization |
| **Memory Explorer** | Institutional knowledge | Full-text search |
| **Similar Cases** | Evidence-based decisions | Historical pattern matching |
| **Live Transactions** | Immediate action | Real-time filtering |
| **Risk Heatmap** | Geographic insights | Map visualization |
| **Analytics** | System monitoring | Team performance tracking |
| **Case Management** | Team collaboration | Status workflow |
| **Feedback Loop** | Continuous improvement | ML retraining pipeline |

---

## 🚀 Post-Demo Actions

1. **Ask for Feedback** - "What's most valuable for your team?"
2. **Show Integration Options** - "How can we connect to your transaction feed?"
3. **Discuss Customization** - "What metrics matter most?"
4. **Plan Next Steps** - "Timeline for pilot program?"
5. **Provide Documentation** - Share README, SETUP_GUIDE, ARCHITECTURE

---

## 📊 Demo Metrics to Highlight

- **System Accuracy**: 89.5% on similar cases
- **Analysis Speed**: 3-5 seconds per transaction (Groq enabled)
- **Pattern Detection**: 3 synthetic ID clusters detected
- **Analyst Efficiency**: 18% detection lift from learned patterns
- **Coverage**: 1,230+ transactions analyzed
- **Team Size**: 3 analysts in queue

---

## 🎓 Advanced Demo Topics (Optional)

### For Security Teams
- Explain fraud detection ML models
- Show decision logic and transparency
- Discuss audit trails and compliance

### For Data Teams
- Walk through database schema
- Explain data pipeline
- Show analytics queries

### For Engineers
- Review API design and RESTful principles
- Discuss error handling and validation
- Explain database relationships

---

**Status**: ✅ Demo script complete | Ready to present!

**Estimated Total Time**: 60-90 minutes
**Flexibility**: Can shorten to 30 min or extend to 2 hours
