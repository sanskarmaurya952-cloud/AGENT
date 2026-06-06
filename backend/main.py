from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
import os
import logging
from groq import Groq
from uuid import uuid4

from backend.database import SessionLocal, init_db
from backend.models import Investigation, Memory, Transaction, HindsightMemory
from backend.schemas import MemorySearchRequest, MemoryStoreRequest, InvestigateTransactionRequest, InvestigationReport, AnalystFeedbackRequest, HindsightMemoryResponse, SimilarCasesContext

# Setup logging
logger = logging.getLogger(__name__)

# Configuration from environment
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Risk Intelligence API",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

# Add CORS middleware with environment-based origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Startup event handler with environment validation."""
    # Initialize database
    init_db()
    seed_db()
    
    # Log startup information
    logger.info("Application startup complete")
    
    # Warn about missing optional configurations
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not configured - using fallback rule-based analysis")
    
    if not DATABASE_URL:
        logger.warning("DATABASE_URL not configured - using mock data mode")


def seed_db() -> None:
    if SessionLocal is None:
        return

    with SessionLocal() as db:
        if db.query(Transaction).first() is not None:
            return

        transactions = [
            Transaction(
                customer="Nadia Chen",
                amount=249.95,
                currency="USD",
                location="Singapore",
                merchant="Northwind Electronics",
                risk="Critical",
                status="review",
                action="Review",
                risk_score=82,
            ),
            Transaction(
                customer="Ethan Brooks",
                amount=18.4,
                currency="USD",
                location="London",
                merchant="Harbor Coffee",
                risk="High",
                status="clear",
                action="Investigate",
                risk_score=12,
            ),
            Transaction(
                customer="Ava Patel",
                amount=1599.0,
                currency="USD",
                location="New York",
                merchant="Orbit Mobility",
                risk="Medium",
                status="escalated",
                action="Monitor",
                risk_score=94,
            ),
        ]

        db.add_all(transactions)
        db.flush()

        investigations = [
            Investigation(transaction_id=transactions[0].id, status="open", severity="high", assigned_to="Analyst 1", summary="Velocity spike tied to repeated device usage."),
            Investigation(transaction_id=transactions[1].id, status="open", severity="medium", assigned_to="Analyst 2", summary="Low-risk transaction monitored for pattern drift."),
            Investigation(transaction_id=transactions[2].id, status="investigating", severity="high", assigned_to="Analyst 3", summary="Escalated transaction with geographic anomaly."),
        ]

        memories = [
            Memory(
                investigation=investigations[0],
                title="Synthetic identity ring",
                content="Synthetic identity cluster matched prior device reuse and merchant behavior patterns.",
                risk_level="Critical",
                fraud_type="Identity Fraud",
                confidence=0.96,
                learning_impact="+18% detection lift",
            ),
            Memory(
                investigation=investigations[1],
                title="Merchant collusion cluster",
                content="Merchant collusion indicators expanded the historical pattern library.",
                risk_level="High",
                fraud_type="Merchant Abuse",
                confidence=0.91,
                learning_impact="+11% pattern recall",
            ),
            Memory(
                investigation=investigations[2],
                title="Cross-border mule route",
                content="Cross-border mule routing pattern reinforced in the learning graph.",
                risk_level="Critical",
                fraud_type="Money Laundering",
                confidence=0.98,
                learning_impact="+23% alert precision",
            ),
        ]

        db.add_all(investigations + memories)
        db.commit()


def memory_to_payload(memory: Memory) -> dict:
    return {
        "id": memory.id,
        "investigat -> dictionId": memory.investigation_id,
        "title": memory.title,
        "content": memory.content,
        "riskLevel": memory.risk_level,
        "fraudType": memory.fraud_type,
        "confidence": memory.confidence,
        "learningImpact": memory.learning_impact or "",
        "createdAt": memory.created_at.isoformat(),
    }


@app.get("/dashboard")
def get_dashboard():
    if SessionLocal is None:
        return {
            "kpis": [
                {"label": "Total Transactions", "value": "18,420", "delta": "+12.4%", "tone": "cyan"},
                {"label": "Fraud Cases", "value": "214", "delta": "-8.2%", "tone": "emerald"},
                {"label": "Risk Score", "value": "82.4", "delta": "+3.1", "tone": "amber"},
                {"label": "Memory Entries", "value": "94.6K", "delta": "+18.9%", "tone": "blue"},
            ],
            "summary": {
                "totalTransactions": 18420,
                "flaggedTransactions": 214,
                "highRiskAlerts": 17,
                "analystQueue": 9,
            },
            "trend": [
                {"date": "2026-06-01", "transactions": 4210, "flags": 39},
                {"date": "2026-06-02", "transactions": 4395, "flags": 44},
                {"date": "2026-06-03", "transactions": 4520, "flags": 51},
                {"date": "2026-06-04", "transactions": 4295, "flags": 40},
            ],
            "topInsights": [
                "Unusual cross-border activity increased during the last 24 hours.",
                "Card-not-present transactions remain the dominant risk pattern.",
                "A small cluster of repeat devices is driving most alerts.",
            ],
            "memoryCards": [],
        }

    with SessionLocal() as db:
        transactions = db.query(Transaction).all()
        investigations = db.query(Investigation).all()
        memories = db.query(Memory).all()

        flagged_transactions = sum(1 for transaction in transactions if transaction.risk_score >= 80)
        high_risk_alerts = sum(1 for investigation in investigations if investigation.severity == "high")
        total_memory_count = len(memories)

        return {
            "kpis": [
                {"label": "Total Transactions", "value": f"{len(transactions):,}", "delta": "+12.4%", "tone": "cyan"},
                {"label": "Fraud Cases", "value": f"{flagged_transactions:,}", "delta": "-8.2%", "tone": "emerald"},
                {"label": "Risk Score", "value": "82.4", "delta": "+3.1", "tone": "amber"},
                {"label": "Memory Entries", "value": f"{total_memory_count:,}", "delta": "+18.9%", "tone": "blue"},
            ],
            "summary": {
                "totalTransactions": len(transactions),
                "flaggedTransactions": flagged_transactions,
                "highRiskAlerts": high_risk_alerts,
                "analystQueue": len(investigations),
            },
            "trend": [
                {"date": "2026-06-01", "transactions": 4210, "flags": 39},
                {"date": "2026-06-02", "transactions": 4395, "flags": 44},
                {"date": "2026-06-03", "transactions": 4520, "flags": 51},
                {"date": "2026-06-04", "transactions": 4295, "flags": 40},
            ],
            "topInsights": [
                "Unusual cross-border activity increased during the last 24 hours.",
                "Card-not-present transactions remain the dominant risk pattern.",
                "A small cluster of repeat devices is driving most alerts.",
            ],
            "memoryCards": [
                {
                    "title": memory.title,
                    "riskLevel": memory.risk_level,
                    "fraudType": memory.fraud_type,
                    "confidence": memory.confidence,
                    "date": memory.created_at.date().isoformat(),
                    "learningImpact": memory.learning_impact or "",
                }
                for memory in memories
            ],
        }


@app.get("/transactions")
def get_transactions() -> dict:
    if SessionLocal is None:
        return {
            "items": [
                {
                    "id": "txn_1001",
                    "customer": "Nadia Chen",
                    "amount": 249.95,
                    "currency": "USD",
                    "location": "Singapore",
                    "merchant": "Northwind Electronics",
                    "risk": "Critical",
                    "status": "review",
                    "action": "Review",
                    "riskScore": 82,
                },
                {
                    "id": "txn_1002",
                    "customer": "Ethan Brooks",
                    "amount": 18.4,
                    "currency": "USD",
                    "location": "London",
                    "merchant": "Harbor Coffee",
                    "risk": "High",
                    "status": "clear",
                    "action": "Investigate",
                    "riskScore": 12,
                },
                {
                    "id": "txn_1003",
                    "customer": "Ava Patel",
                    "amount": 1599.0,
                    "currency": "USD",
                    "location": "New York",
                    "merchant": "Orbit Mobility",
                    "risk": "Medium",
                    "status": "escalated",
                    "action": "Monitor",
                    "riskScore": 94,
                },
            ],
            "page": 1,
            "pageSize": 3,
            "total": 3,
        }

    with SessionLocal() as db:
        transactions = db.query(Transaction).order_by(Transaction.created_at.asc()).all()
        return {
            "items": [
                {
                    "id": transaction.id,
                    "customer": transaction.customer,
                    "amount": transaction.amount,
                    "currency": transaction.currency,
                    "location": transaction.location,
                    "merchant": transaction.merchant,
                    "risk": transaction.risk,
                    "status": transaction.status,
                    "action": transaction.action,
                    "riskScore": transaction.risk_score,
                }
                for transaction in transactions
            ],
            "page": 1,
            "pageSize": len(transactions),
            "total": len(transactions),
        }


@app.get("/alerts")
def get_alerts() -> dict:
    if SessionLocal is None:
        return {
            "items": [
                {
                    "id": "alert_2001",
                    "type": "velocity",
                    "severity": "high",
                    "message": "Multiple transactions detected from the same device within 3 minutes.",
                    "status": "open",
                    "time": "2m ago",
                },
                {
                    "id": "alert_2002",
                    "type": "geo_anomaly",
                    "severity": "medium",
                    "message": "Transaction location changed across distant regions in a short window.",
                    "status": "open",
                    "time": "7m ago",
                },
                {
                    "id": "alert_2003",
                    "type": "merchant_risk",
                    "severity": "low",
                    "message": "Merchant shows a slightly elevated dispute pattern.",
                    "status": "investigating",
                    "time": "15m ago",
                },
            ]
        }

    with SessionLocal() as db:
        investigations = db.query(Investigation).order_by(Investigation.created_at.asc()).all()
        return {
            "items": [
                {
                    "id": investigation.id,
                    "type": investigation.severity,
                    "severity": investigation.severity,
                    "message": investigation.summary or "Investigation in progress.",
                    "status": investigation.status,
                    "time": investigation.created_at.strftime("%dm ago"),
                }
                for investigation in investigations
            ]
        }


@app.post("/memory/store")
def store_memory(payload: MemoryStoreRequest) -> dict:
    if SessionLocal is None:
        raise HTTPException(status_code=503, detail="PostgreSQL is not configured.")

    with SessionLocal() as db:
        if payload.investigation_id is not None:
            if db.get(Investigation, payload.investigation_id) is None:
                raise HTTPException(status_code=404, detail="Investigation not found.")

        memory = Memory(
            investigation_id=payload.investigation_id,
            title=payload.title,
            content=payload.content,
            risk_level=payload.risk_level,
            fraud_type=payload.fraud_type,
            confidence=payload.confidence,
            learning_impact=payload.learning_impact,
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)

        return {"memory": memory_to_payload(memory)}


@app.get("/memories")
def get_memories(limit: int = 25) -> dict:
    if SessionLocal is None:
        # Return mock memory data when database not configured
        return {
            "items": [
                {
                    "id": "mem_1001",
                    "investigationId": "inv_1001",
                    "title": "Synthetic identity ring",
                    "content": "Synthetic identity cluster matched prior device reuse and merchant behavior patterns. High-value transactions detected across multiple accounts.",
                    "riskLevel": "Critical",
                    "fraudType": "Identity Fraud",
                    "confidence": 0.96,
                    "learningImpact": "+18% detection lift",
                    "createdAt": "2026-06-04T10:30:00",
                },
                {
                    "id": "mem_1002",
                    "investigationId": "inv_1002",
                    "title": "Merchant collusion cluster",
                    "content": "Merchant collusion indicators expanded the historical pattern library. Suspicious correlation with Chinese payment channels.",
                    "riskLevel": "High",
                    "fraudType": "Merchant Abuse",
                    "confidence": 0.91,
                    "learningImpact": "+11% pattern recall",
                    "createdAt": "2026-06-04T09:15:00",
                },
                {
                    "id": "mem_1003",
                    "investigationId": "inv_1003",
                    "title": "Cross-border mule route",
                    "content": "Cross-border mule routing pattern reinforced in the learning graph. Consistent with known smuggling networks.",
                    "riskLevel": "Critical",
                    "fraudType": "Money Laundering",
                    "confidence": 0.98,
                    "learningImpact": "+23% alert precision",
                    "createdAt": "2026-06-03T14:22:00",
                },
            ],
            "total": 3,
        }

    with SessionLocal() as db:
        memories = db.query(Memory).order_by(Memory.created_at.desc()).limit(limit).all()
        return {
            "items": [memory_to_payload(memory) for memory in memories],
            "total": db.query(Memory).count(),
        }


@app.post("/memory/search")
def search_memory(payload: MemorySearchRequest) -> dict:
    """Search for fraud patterns in memory database with error handling."""
    # Mock data for search when database not configured
    all_memories = [
        {
            "id": "mem_1001",
            "investigationId": "inv_1001",
            "title": "Synthetic identity ring",
            "content": "Synthetic identity cluster matched prior device reuse and merchant behavior patterns. High-value transactions detected across multiple accounts.",
            "riskLevel": "Critical",
            "fraudType": "Identity Fraud",
            "confidence": 0.96,
            "learningImpact": "+18% detection lift",
            "createdAt": "2026-06-04T10:30:00",
        },
        {
            "id": "mem_1002",
            "investigationId": "inv_1002",
            "title": "Merchant collusion cluster",
            "content": "Merchant collusion indicators expanded the historical pattern library. Suspicious correlation with Chinese payment channels.",
            "riskLevel": "High",
            "fraudType": "Merchant Abuse",
            "confidence": 0.91,
            "learningImpact": "+11% pattern recall",
            "createdAt": "2026-06-04T09:15:00",
        },
        {
            "id": "mem_1003",
            "investigationId": "inv_1003",
            "title": "Cross-border mule route",
            "content": "Cross-border mule routing pattern reinforced in the learning graph. Consistent with known smuggling networks.",
            "riskLevel": "Critical",
            "fraudType": "Money Laundering",
            "confidence": 0.98,
            "learningImpact": "+23% alert precision",
            "createdAt": "2026-06-03T14:22:00",
        },
    ]

    if SessionLocal is None:
        # Perform mock search on all memories
        try:
            query_text = payload.query.strip().lower()
            filtered = [
                m for m in all_memories
                if query_text in m["title"].lower()
                or query_text in m["content"].lower()
                or query_text in m["fraudType"].lower()
                or query_text in m["riskLevel"].lower()
            ]
            logger.info(f"Memory search (mock): query='{payload.query}', results={len(filtered)}")
            return {
                "query": query_text,
                "count": len(filtered),
                "items": filtered[:payload.limit],
            }
        except Exception as e:
            logger.error(f"Error in mock memory search: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")

    try:
        with SessionLocal() as db:
            query_text = payload.query.strip()
            normalized_query = f"%{query_text.lower()}%"

            memories = (
                db.query(Memory)
                .outerjoin(Investigation)
                .filter(
                    or_(
                        Memory.title.ilike(normalized_query),
                        Memory.content.ilike(normalized_query),
                        Memory.fraud_type.ilike(normalized_query),
                        Memory.risk_level.ilike(normalized_query),
                        Investigation.summary.ilike(normalized_query),
                    )
                )
                .order_by(Memory.created_at.desc())
                .limit(payload.limit)
                .all()
            )

            logger.info(f"Memory search: query='{payload.query}', results={len(memories)}")
            return {
                "query": query_text,
                "count": len(memories),
                "items": [memory_to_payload(memory) for memory in memories],
            }
    except Exception as e:
        logger.error(f"Error in database memory search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")


@app.post("/investigate")
def investigate_transaction(payload: InvestigateTransactionRequest) -> InvestigationReport:
    """
    Investigate a transaction using Groq AI + memory search.
    Workflow: Transaction → Memory Search → LLM Analysis → Investigation Report
    """
    
    # Step 1: Search for similar memories
    query_text = f"{payload.merchant} {payload.location} {payload.customer}"
    
    all_mock_memories = [
        {
            "id": "mem_1001",
            "title": "Synthetic identity ring",
            "fraudType": "Identity Fraud",
            "riskLevel": "Critical",
            "confidence": 0.96,
            "content": "Synthetic identity cluster matched prior device reuse and merchant behavior patterns.",
        },
        {
            "id": "mem_1002",
            "title": "Merchant collusion cluster",
            "fraudType": "Merchant Abuse",
            "riskLevel": "High",
            "confidence": 0.91,
            "content": "Merchant collusion indicators expanded the historical pattern library.",
        },
        {
            "id": "mem_1003",
            "title": "Cross-border mule route",
            "fraudType": "Money Laundering",
            "riskLevel": "Critical",
            "confidence": 0.98,
            "content": "Cross-border mule routing pattern reinforced in the learning graph.",
        },
    ]
    
    similar_memories = []
    if SessionLocal is None:
        # Mock memory search
        query_lower = query_text.lower()
        similar_memories = [
            m for m in all_mock_memories
            if query_lower in m.get("title", "").lower()
            or query_lower in m.get("content", "").lower()
        ]
        if not similar_memories:
            similar_memories = all_mock_memories[:2]  # Return top 2 if no match
    else:
        with SessionLocal() as db:
            query_normalized = f"%{query_text.lower()}%"
            db_memories = (
                db.query(Memory)
                .filter(
                    or_(
                        Memory.title.ilike(query_normalized),
                        Memory.content.ilike(query_normalized),
                        Memory.fraud_type.ilike(query_normalized),
                    )
                )
                .limit(5)
                .all()
            )
            similar_memories = [
                {
                    "id": str(m.id),
                    "title": m.title,
                    "fraudType": m.fraud_type,
                    "riskLevel": m.risk_level,
                    "confidence": m.confidence,
                    "content": m.content,
                }
                for m in db_memories
            ]
    
    # Step 2: Build context for Groq
    memories_context = ""
    if similar_memories:
        memories_context = "Related past fraud cases:\n"
        for mem in similar_memories[:3]:
            memories_context += f"- {mem.get('title', 'Unknown')}: {mem.get('content', '')} (Risk: {mem.get('riskLevel')}, Confidence: {mem.get('confidence', 0):.0%})\n"
    
    transaction_summary = f"""
Transaction Details:
- ID: {payload.transaction_id}
- Customer: {payload.customer}
- Amount: {payload.currency} {payload.amount:,.2f}
- Location: {payload.location}
- Merchant: {payload.merchant}
- Initial Risk Score: {payload.risk_score}/100
"""
    
    # Step 3: Call Groq API for analysis
    if not GROQ_API_KEY:
        # Fallback: rule-based analysis without Groq
        risk_level = "Critical" if payload.risk_score >= 80 else "High" if payload.risk_score >= 60 else "Medium" if payload.risk_score >= 40 else "Low"
        confidence = min(0.95, (payload.risk_score / 100) + 0.1)
        fraud_type = "Unknown"
        
        if similar_memories:
            fraud_type = similar_memories[0].get("fraudType", "Unknown")
        
        logger.info(f"Investigation (rule-based): txn={payload.transaction_id}, risk={risk_level}")
        return InvestigationReport(
            transaction_id=payload.transaction_id,
            risk_level=risk_level,
            confidence=confidence,
            fraud_type=fraud_type,
            reasoning=f"Transaction flagged due to high risk score ({payload.risk_score}) and {len(similar_memories)} related past fraud cases. " +
                     (f"Most relevant: {similar_memories[0].get('title')}" if similar_memories else "No prior history."),
            related_memories=len(similar_memories),
            recommended_action="Review" if risk_level in ["Critical", "High"] else "Monitor",
            investigation_notes=f"Groq API not configured. Analysis based on rule engine and {len(similar_memories)} similar memories."
        )
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""You are a fraud investigation expert. Analyze this transaction and provide a risk assessment.

{transaction_summary}

{memories_context}

Based on the transaction details and similar past cases, provide:
1. Risk Level (Critical/High/Medium/Low)
2. Fraud Type (e.g., Identity Fraud, Merchant Abuse, Money Laundering, Card Fraud, Account Takeover)
3. Confidence score (0-100%)
4. Reasoning (2-3 sentences explaining the risk)
5. Recommended Action (Review/Investigate/Monitor/Clear)
6. Investigation Notes (any patterns or anomalies detected)

Format your response as:
RISK_LEVEL: [level]
FRAUD_TYPE: [type]
CONFIDENCE: [score]%
REASONING: [reasoning]
RECOMMENDED_ACTION: [action]
INVESTIGATION_NOTES: [notes]"""
        
        message = client.messages.create(
            model="mixtral-8x7b-32768",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse response
        lines = response_text.split("\n")
        parsed = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                parsed[key.strip()] = value.strip()
        
        risk_level = parsed.get("RISK_LEVEL", "Medium")
        fraud_type = parsed.get("FRAUD_TYPE", "Unknown")
        confidence_str = parsed.get("CONFIDENCE", "50%").replace("%", "").strip()
        confidence = float(confidence_str) / 100 if confidence_str.isdigit() else 0.5
        reasoning = parsed.get("REASONING", "Analysis completed by AI.")
        recommended_action = parsed.get("RECOMMENDED_ACTION", "Review")
        investigation_notes = parsed.get("INVESTIGATION_NOTES", "")
        
        return InvestigationReport(
            transaction_id=payload.transaction_id,
            risk_level=risk_level,
            confidence=min(1.0, confidence),
            fraud_type=fraud_type,
            reasoning=reasoning,
            related_memories=len(similar_memories),
            recommended_action=recommended_action,
            investigation_notes=investigation_notes
        )
    
    except Exception as e:
        # Fallback on API error
        return InvestigationReport(
            transaction_id=payload.transaction_id,
            risk_level="High" if payload.risk_score >= 70 else "Medium",
            confidence=0.7,
            fraud_type=similar_memories[0].get("fraudType", "Unknown") if similar_memories else "Unknown",
            reasoning=f"Groq analysis attempted but encountered error. Flagged due to risk score {payload.risk_score} and {len(similar_memories)} similar cases.",
            related_memories=len(similar_memories),
            recommended_action="Review",
            investigation_notes=f"Error: {str(e)}. Using fallback analysis."
        )


@app.post("/feedback", response_model=HindsightMemoryResponse)
def submit_analyst_feedback(payload: AnalystFeedbackRequest) -> HindsightMemoryResponse:
    """Store analyst feedback on investigation outcome for hindsight learning."""
    if SessionLocal is None:
        return HindsightMemoryResponse(
            memory_id="mock_feedback_" + str(uuid4()),
            feedback_type=payload.feedback_type,
            message=f"Feedback recorded: {payload.feedback_type} for transaction {payload.transaction_id}"
        )
    
    try:
        with SessionLocal() as db:
            # Create hindsight memory record
            hindsight = HindsightMemory(
                investigation_id=payload.investigation_id,
                transaction_id=payload.transaction_id,
                amount=payload.amount,
                location=payload.location,
                merchant=payload.merchant,
                original_risk_level=payload.original_risk_level,
                original_confidence=payload.original_confidence,
                feedback_type=payload.feedback_type,
                analyst_notes=payload.analyst_notes,
                actual_outcome=payload.actual_outcome or payload.feedback_type,
            )
            db.add(hindsight)
            db.commit()
            db.refresh(hindsight)
            
            return HindsightMemoryResponse(
                memory_id=str(hindsight.id),
                feedback_type=hindsight.feedback_type,
                message=f"Hindsight feedback stored successfully. This will improve future fraud detection."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store feedback: {str(e)}")


@app.get("/hindsight/similar-cases", response_model=SimilarCasesContext)
def get_similar_cases(
    amount: float,
    location: str,
    merchant: str,
    limit: int = 5
) -> SimilarCasesContext:
    """Find similar past cases from hindsight memory to inform current investigation."""
    
    if SessionLocal is None:
        # Return mock similar cases
        return SimilarCasesContext(
            similar_cases=[
                {
                    "amount": 245.50,
                    "location": location,
                    "merchant": merchant,
                    "original_risk": "High",
                    "feedback": "confirm_fraud",
                    "outcome": "Transaction reversed, account secured",
                    "date": "2024-05-15"
                },
                {
                    "amount": 189.99,
                    "location": location,
                    "merchant": "Similar Merchant",
                    "original_risk": "Medium",
                    "feedback": "false_positive",
                    "outcome": "Transaction cleared, customer satisfied",
                    "date": "2024-05-10"
                }
            ],
            accuracy_rate=89.5,
            common_patterns=[
                "Velocity spike from new device",
                "Geographic mismatch with usual activity",
                "Merchant category change"
            ]
        )
    
    try:
        with SessionLocal() as db:
            # Find similar hindsight memories within range
            similar_hindsight = (
                db.query(HindsightMemory)
                .filter(
                    HindsightMemory.location == location,
                    HindsightMemory.merchant.ilike(f"%{merchant}%") | HindsightMemory.merchant == merchant,
                )
                .order_by(HindsightMemory.created_at.desc())
                .limit(limit)
                .all()
            )
            
            # Convert to similar cases
            similar_cases = [
                {
                    "amount": h.amount,
                    "location": h.location,
                    "merchant": h.merchant,
                    "original_risk": h.original_risk_level,
                    "feedback": h.feedback_type,
                    "outcome": h.actual_outcome,
                    "date": h.created_at.isoformat()
                }
                for h in similar_hindsight
            ]
            
            # Calculate accuracy from feedback
            if similar_hindsight:
                correct_predictions = len([h for h in similar_hindsight if h.feedback_type == "confirm_fraud"])
                accuracy_rate = (correct_predictions / len(similar_hindsight)) * 100
            else:
                accuracy_rate = 0.0
            
            return SimilarCasesContext(
                similar_cases=similar_cases,
                accuracy_rate=min(100.0, accuracy_rate),
                common_patterns=[
                    f"Merchant: {merchant}",
                    f"Location: {location}",
                    "Historical feedback available"
                ]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve similar cases: {str(e)}")