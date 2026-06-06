# Quick Start Guide: POST /investigate/groq Endpoint

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Test Endpoint (in another terminal)
```bash
curl -X POST http://localhost:8000/investigate/groq \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "location": "Dubai",
    "merchant": "Unknown Merchant"
  }'
```

## 📊 Example Requests & Responses

### Example 1: High-Risk Transaction
```bash
curl -X POST http://localhost:8000/investigate/groq \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "location": "Dubai",
    "merchant": "Unknown Merchant"
  }'
```

**Response (200 OK):**
```json
{
  "risk_level": "High",
  "investigation_summary": "Large high-value transaction ($50,000) detected from Dubai to an unknown merchant...",
  "recommended_action": "Investigate",
  "confidence_score": 80,
  "fraud_indicators": [
    "Large transaction amount ($50,000+)",
    "International high-risk location",
    "Unverified/Unknown merchant"
  ],
  "analysis_timestamp": "2026-06-05T10:30:45.123456Z"
}
```

### Example 2: Low-Risk Transaction
```bash
curl -X POST http://localhost:8000/investigate/groq \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2500,
    "location": "New York",
    "merchant": "Amazon"
  }'
```

**Response:**
```json
{
  "risk_level": "Low",
  "investigation_summary": "Standard domestic transaction within normal parameters...",
  "recommended_action": "Clear",
  "confidence_score": 15,
  "fraud_indicators": ["Standard transaction pattern"],
  "analysis_timestamp": "2026-06-05T10:31:20.456789Z"
}
```

## 🧪 Run Tests

### All Tests
```bash
python -m pytest backend/test_*.py -v
```

### Specific Test Suite
```bash
# Test Groq integration
python -m pytest backend/test_groq_integration.py -v

# Test FastAPI endpoints
python -m pytest backend/test_main.py -v

# Test logic directly (no server needed)
python backend/test_production_endpoint.py
```

## 📝 API Specification

### Endpoint
```
POST /investigate/groq
```

### Request
```json
{
  "amount": 50000,
  "location": "Dubai",
  "merchant": "Unknown Merchant"
}
```

### Response
```json
{
  "risk_level": "Critical|High|Medium|Low",
  "investigation_summary": "string",
  "recommended_action": "Review|Investigate|Monitor|Clear",
  "confidence_score": 0-100,
  "fraud_indicators": ["string"],
  "analysis_timestamp": "ISO 8601 UTC"
}
```

## 🔧 Integration Example (Python)

```python
import requests

def check_transaction_fraud(amount, location, merchant):
    """Check if transaction is fraudulent."""
    
    url = "http://localhost:8000/investigate/groq"
    payload = {
        "amount": amount,
        "location": location,
        "merchant": merchant
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Risk Level: {result['risk_level']}")
        print(f"Action: {result['recommended_action']}")
        print(f"Confidence: {result['confidence_score']}%")
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
result = check_transaction_fraud(50000, "Dubai", "Unknown Merchant")
```

## ⚠️ Common Issues & Solutions

### Issue: Connection Refused (Cannot connect to localhost:8000)
**Solution:**
1. Make sure server is running: `uvicorn main:app --reload --port 8000`
2. Check port 8000 is not in use: `netstat -ano | findstr :8000`
3. Try different port: `uvicorn main:app --reload --port 8001`

### Issue: 422 Unprocessable Entity
**Solution:**
Check request JSON:
- `amount` must be > 0
- `location` must not be empty
- `merchant` must not be empty
All three fields are required.

### Issue: Always Getting "Groq API not configured"
**Solution:**
1. Check `.env` file has `GROQ_API_KEY`
2. Restart the server after updating `.env`
3. Verify key is correct

### Issue: Slow Responses (> 5 seconds)
**Solution:**
1. Check Groq API status (may be rate limited)
2. Endpoint falls back to rule-based analysis automatically
3. Monitor network connectivity

## 📚 Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | `{"risk_level": "High", ...}` |
| 400 | Bad JSON | Invalid JSON in request body |
| 422 | Validation Error | `amount: -1000` (negative not allowed) |
| 500 | Server Error | Unexpected backend error |

## 🎯 Test Cases

### Critical Risk (>80%)
```json
{
  "amount": 75000,
  "location": "Hong Kong",
  "merchant": "Unverified Trading LLC"
}
```
Expected: `Critical` / `Review`

### High Risk (60-80%)
```json
{
  "amount": 50000,
  "location": "Dubai",
  "merchant": "Unknown Merchant"
}
```
Expected: `High` / `Investigate`

### Medium Risk (40-60%)
```json
{
  "amount": 8000,
  "location": "Singapore",
  "merchant": "Generic Electronics"
}
```
Expected: `Medium` / `Monitor`

### Low Risk (<40%)
```json
{
  "amount": 2500,
  "location": "New York",
  "merchant": "Amazon"
}
```
Expected: `Low` / `Clear`

## 🔍 Response Structure Details

### risk_level
One of: `Critical`, `High`, `Medium`, `Low`
- Based on transaction amount, location, merchant

### investigation_summary
2-3 sentence detailed analysis explaining the risk assessment

### recommended_action
One of: `Review`, `Investigate`, `Monitor`, `Clear`
- `Review`: Critical/High risk - immediate action
- `Investigate`: High risk - detailed investigation
- `Monitor`: Medium risk - keep under observation
- `Clear`: Low risk - approve transaction

### confidence_score
0-100 percentage indicating confidence in the assessment

### fraud_indicators
List of 1-5 specific fraud patterns detected:
- "Large transaction amount ($50,000+)"
- "International high-risk location"
- "Unverified/Unknown merchant"
- etc.

### analysis_timestamp
ISO 8601 UTC timestamp of when analysis was performed
Format: `2026-06-05T10:30:45.123456Z`

## 📖 Documentation Files

- `GROQ_ENDPOINT_README.md` - Comprehensive endpoint documentation
- `IMPLEMENTATION_SUMMARY.md` - Detailed implementation overview
- `QUICKSTART.md` - This file

## 🎓 Learn More

### API Documentation
```
GET /docs
```
Access at: `http://localhost:8000/docs`
(Note: OpenAPI docs are disabled in current config)

### Test Files
- `backend/test_production_endpoint.py` - Best for learning the logic
- `backend/test_groq_endpoint.py` - HTTP integration examples
- `backend/test_groq_integration.py` - Comprehensive test cases

## ✅ Verification Checklist

- [ ] Backend installed: `pip install -r requirements.txt`
- [ ] `.env` file has `GROQ_API_KEY`
- [ ] Server running: `uvicorn main:app --reload --port 8000`
- [ ] Can access endpoint: `curl http://localhost:8000/investigate/groq`
- [ ] Returns valid JSON response
- [ ] All test cases pass: `pytest backend/test_*.py -v`

## 🚀 You're Ready!

The endpoint is production-ready and fully tested. Start using it to analyze transactions for fraud risk.

---

**Need Help?**
1. Check server logs: `uvicorn main:app --reload --port 8000` (verbose output)
2. Run test: `python backend/test_production_endpoint.py`
3. Review: `GROQ_ENDPOINT_README.md` for detailed documentation
