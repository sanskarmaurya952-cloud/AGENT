# Analyst Feedback System - Hindsight Memory

## Overview

The Analyst Feedback System enables fraud investigators to record their findings on investigation outcomes, which are stored in **Hindsight Memory**. This feedback is then used to improve future fraud investigations through machine learning and pattern recognition.

## Features

### 1. Feedback Buttons (UI)
Three feedback options are presented after each investigation:

- **Confirm Fraud** (Red) - Transaction was confirmed to be fraudulent
- **False Positive** (Yellow) - Investigation was incorrect; transaction is legitimate
- **Legitimate** (Green) - Transaction was confirmed to be legitimate

### 2. Hindsight Memory Storage
When analysts provide feedback, the system stores:

```
- Investigation ID & Transaction ID
- Transaction details (amount, location, merchant)
- Original investigation outcome (risk level, confidence)
- Analyst feedback type (confirm_fraud, false_positive, legitimate)
- Optional analyst notes
- Actual outcome determination
- Timestamp
```

### 3. Pattern Learning
Future investigations use hindsight memory to:

- Find similar past cases with feedback
- Calculate accuracy rates based on feedback type
- Extract common patterns in merchant/location/amount ranges
- Provide context to improve current investigations

## API Endpoints

### POST /feedback
Submit analyst feedback on an investigation.

**Request:**
```json
{
  "investigation_id": "inv_txn_1001_1717590645000",
  "transaction_id": "txn_1001",
  "amount": 50000,
  "location": "Dubai",
  "merchant": "Unknown Merchant",
  "original_risk_level": "High",
  "original_confidence": 80,
  "feedback_type": "confirm_fraud",
  "analyst_notes": "Customer confirmed unauthorized transaction",
  "actual_outcome": "Merchant charged without authorization - confirmed fraud"
}
```

**Response:**
```json
{
  "memory_id": "hm_uuid_xyz",
  "feedback_type": "confirm_fraud",
  "message": "Analyst feedback recorded: confirm_fraud"
}
```

**Status Codes:**
- `200 OK` - Feedback stored successfully
- `400 Bad Request` - Invalid feedback type
- `500 Internal Server Error` - Database error

### GET /hindsight/similar-cases
Query similar cases from hindsight memory.

**Parameters:**
- `amount` (float) - Transaction amount
- `location` (string) - Transaction location
- `merchant` (string) - Merchant name
- `limit` (int, default=5) - Max cases to return

**Response:**
```json
{
  "similar_cases": [
    {
      "amount": 48500,
      "location": "Dubai",
      "merchant": "Dubai Merchant",
      "original_risk": "High",
      "feedback": "confirm_fraud",
      "outcome": "Merchant charged without authorization - confirmed fraud",
      "date": "2026-05-24T10:30:00Z"
    }
  ],
  "accuracy_rate": 85.5,
  "common_patterns": [
    "Similar cases often confirmed as fraud (4/5)",
    "Location Dubai has history in similar cases",
    "Merchant type patterns match with 3 similar cases"
  ]
}
```

## Frontend Integration

### Component: AI Investigator
Located in `components/ai/ai-investigator.tsx`

**Features:**
1. Displays investigation results from Groq AI
2. Shows three feedback buttons below recommendations
3. Handles feedback submission asynchronously
4. Displays success/error messages
5. Shows fraud indicators from investigation

**Feedback Button Actions:**
```typescript
// Example: Confirming fraud
await submitAnalystFeedback({
  investigation_id: "inv_txn_1001_...",
  transaction_id: "txn_1001",
  amount: 50000,
  location: "Dubai",
  merchant: "Unknown Merchant",
  original_risk_level: "High",
  original_confidence: 80,
  feedback_type: "confirm_fraud"
});
```

## Database Schema

### HindsightMemory Table
```sql
CREATE TABLE hindsight_memories (
  id VARCHAR(36) PRIMARY KEY,
  investigation_id VARCHAR(36) NOT NULL,
  transaction_id VARCHAR(36) NOT NULL,
  
  -- Transaction context
  amount FLOAT NOT NULL,
  location VARCHAR(255) NOT NULL,
  merchant VARCHAR(255) NOT NULL,
  
  -- Original investigation
  original_risk_level VARCHAR(50) NOT NULL,
  original_confidence FLOAT NOT NULL,
  
  -- Analyst feedback
  feedback_type VARCHAR(50) NOT NULL,  -- confirm_fraud, false_positive, legitimate
  analyst_notes TEXT,
  actual_outcome VARCHAR(100) NOT NULL,
  
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

**Indexes:**
- `investigation_id` - Quick lookup by investigation
- `transaction_id` - Quick lookup by transaction
- `created_at` - Time-based queries
- `amount` range queries for similarity matching

## Use Cases

### Case 1: Confirming Fraud Detection
```
Scenario: Groq flagged $50K Dubai transaction as High risk
Analyst: Reviews and confirms it was actual fraud
Action: Clicks "Confirm Fraud" button
Result: Memory stored → Future similar cases get +confidence boost
```

### Case 2: Reducing False Positives
```
Scenario: Groq flagged $5K London transaction as Medium risk
Analyst: Investigates and finds customer confirmed legitimate purchase
Action: Clicks "False Positive" button
Result: Memory stored → Future London transactions are weighted lower
```

### Case 3: Legitimate Transactions
```
Scenario: Groq flagged $100K Singapore merchant as High risk
Analyst: Confirms it's a known business relationship
Action: Clicks "Legitimate" button
Result: Memory stored → Similar Singapore merchants get reduced suspicion
```

## Accuracy Tracking

The system calculates accuracy rates for each feedback type:

```
Confirm Fraud Accuracy = (Cases correctly identified as fraud / Total confirm_fraud feedback)
False Positive Rate = (Cases correctly ruled out / Total false_positive feedback)
Legitimate Rate = (Cases correctly verified / Total legitimate feedback)
```

These accuracy rates are used to:
- Weight future investigations
- Identify analyst patterns
- Improve model training
- Track system performance

## Pattern Recognition

### Location-Based Patterns
```
Example: Dubai transactions with unknown merchants
- Past cases: 10 total
- Confirm fraud: 8 (80%)
- False positive: 1 (10%)
- Legitimate: 1 (10%)
→ Future Dubai + unknown merchant cases get higher fraud weight
```

### Amount-Based Patterns
```
Example: Transactions $45K-$55K
- Past cases: 15 total
- Avg original risk: High
- Avg confidence: 75%
- Actual fraud rate: 85%
→ Similar amounts use past patterns for context
```

### Merchant-Based Patterns
```
Example: Unknown/New merchants
- Past cases: 20 total
- Confirm fraud: 16 (80%)
- False positive: 2 (10%)
- Legitimate: 2 (10%)
→ Unknown merchants weighted higher for risk
```

## Integration with Groq AI

The hindsight memories can be optionally included in the Groq prompt:

```
"Review this transaction and consider these similar past cases:
- Case 1: $48K Dubai unknown merchant → confirmed fraud (80% similar)
- Case 2: $52K Dubai new merchant → confirmed fraud (78% similar)

This context suggests high fraud probability for unknown merchants in Dubai.
```

## Testing the System

### Manual Testing

1. **Start Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Submit Feedback:**
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "investigation_id": "inv_test_1",
    "transaction_id": "txn_test_1",
    "amount": 50000,
    "location": "Dubai",
    "merchant": "Test Merchant",
    "original_risk_level": "High",
    "original_confidence": 80,
    "feedback_type": "confirm_fraud",
    "actual_outcome": "Confirmed fraud - unauthorized charge"
  }'
```

3. **Query Similar Cases:**
```bash
curl -X GET "http://localhost:8000/hindsight/similar-cases?amount=50000&location=Dubai&merchant=Test&limit=5"
```

### Automated Testing

Create `backend/test_feedback_system.py`:
```python
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_submit_feedback():
    response = client.post("/feedback", json={
        "investigation_id": "inv_test_1",
        "transaction_id": "txn_test_1",
        "amount": 50000,
        "location": "Dubai",
        "merchant": "Test Merchant",
        "original_risk_level": "High",
        "original_confidence": 80,
        "feedback_type": "confirm_fraud"
    })
    assert response.status_code == 200
    assert response.json()["feedback_type"] == "confirm_fraud"

def test_similar_cases():
    response = client.get("/hindsight/similar-cases?amount=50000&location=Dubai&merchant=Test")
    assert response.status_code == 200
    assert "similar_cases" in response.json()
    assert "accuracy_rate" in response.json()
```

## Best Practices

### For Analysts
1. **Provide detailed notes** - Help future investigations understand context
2. **Verify before feedback** - Ensure investigation outcome is correct
3. **Note special circumstances** - Exception cases help pattern recognition
4. **Use consistent feedback** - Similar findings should use same classification

### For System
1. **Weight recent feedback** - Newer patterns more relevant
2. **Segment by risk level** - Different patterns for critical vs medium risk
3. **Track analyst accuracy** - Identify expert analysts
4. **Audit hindsight memory** - Regular review for quality

## Future Enhancements

1. **Analyst Reputation** - Track accuracy by analyst
2. **Temporal Patterns** - Consider seasonality and trends
3. **Machine Learning** - Use hindsight data for model retraining
4. **Feedback Categories** - More granular feedback types
5. **Case Comparison** - Visual similarity matching interface
6. **Automated Actions** - Auto-adjust risk scores based on patterns
7. **Cross-Merchant Patterns** - Identify fraud rings
8. **Geographic Clustering** - Location-based fraud patterns

## Troubleshooting

### Issue: Feedback not saving
- Check database connection
- Verify investigation_id and transaction_id exist
- Check for required field validation errors

### Issue: Similar cases not returning
- Ensure feedback has been submitted
- Check amount range query (±20%)
- Verify location/merchant strings match exactly

### Issue: Accuracy rate is 0%
- Need more feedback data
- Check feedback_type values
- Verify actual_outcome data

## Files Modified

### Backend
- `backend/models.py` - Added HindsightMemory model
- `backend/schemas.py` - Added AnalystFeedbackRequest, HindsightMemoryResponse, SimilarCasesContext
- `backend/main.py` - Added /feedback and /hindsight/similar-cases endpoints

### Frontend
- `components/ai/ai-investigator.tsx` - Added feedback buttons and submission logic
- `lib/api.ts` - Added submitAnalystFeedback and getSimilarCases functions

### Database
- Automatic table creation via SQLAlchemy on startup

## Performance Notes

- **Similar Case Query:** O(n) database scan with amount range filtering
- **Accuracy Calculation:** O(1) with proper indexing
- **Memory Growth:** ~500 bytes per feedback record
- **Query Latency:** <100ms for typical 1000-record hindsight memory

For large-scale deployments:
- Add vector embeddings for semantic similarity
- Implement caching for accuracy rates
- Use database views for common patterns
- Archive old feedback periodically
