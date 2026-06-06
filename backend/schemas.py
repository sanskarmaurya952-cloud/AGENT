from pydantic import BaseModel, Field


class MemoryStoreRequest(BaseModel):
    investigation_id: str | None = None
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    risk_level: str = Field(min_length=1)
    fraud_type: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    learning_impact: str | None = None


class MemorySearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=25)


class InvestigateTransactionRequest(BaseModel):
    transaction_id: str = Field(min_length=1)
    customer: str = Field(min_length=1)
    amount: float = Field(gt=0)
    currency: str = Field(min_length=1, max_length=3)
    location: str = Field(min_length=1)
    merchant: str = Field(min_length=1)
    risk_score: int = Field(ge=0, le=100)


class InvestigationReport(BaseModel):
    transaction_id: str
    risk_level: str  # Critical, High, Medium, Low
    confidence: float  # 0-1
    fraud_type: str
    reasoning: str
    related_memories: int
    recommended_action: str
    investigation_notes: str


class SimpleInvestigationRequest(BaseModel):
    """Simplified fraud investigation request."""
    amount: float = Field(gt=0, description="Transaction amount")
    location: str = Field(min_length=1, max_length=100, description="Transaction location")
    merchant: str = Field(min_length=1, max_length=200, description="Merchant name")


class InvestigationResult(BaseModel):
    """Fraud investigation result from Groq AI."""
    risk_level: str = Field(description="Risk level: Critical, High, Medium, Low")
    investigation_summary: str = Field(description="Detailed investigation summary")
    recommended_action: str = Field(description="Recommended action: Review, Investigate, Monitor, Clear")
    confidence_score: float = Field(ge=0, le=100, description="Confidence percentage 0-100")
    fraud_indicators: list[str] = Field(description="List of detected fraud indicators")
    analysis_timestamp: str = Field(description="ISO format timestamp of analysis")


class AnalystFeedbackRequest(BaseModel):
    """Analyst feedback on investigation outcome."""
    investigation_id: str = Field(min_length=1, description="Investigation ID")
    transaction_id: str = Field(min_length=1, description="Transaction ID")
    amount: float = Field(gt=0, description="Transaction amount")
    location: str = Field(min_length=1, max_length=100, description="Transaction location")
    merchant: str = Field(min_length=1, max_length=200, description="Merchant name")
    original_risk_level: str = Field(description="Original risk level from investigation")
    original_confidence: float = Field(ge=0, le=100, description="Original confidence score")
    feedback_type: str = Field(description="Feedback: 'confirm_fraud', 'false_positive', or 'legitimate'")
    analyst_notes: str | None = Field(None, description="Optional analyst notes")
    actual_outcome: str | None = Field(None, description="What actually happened with this transaction")


class HindsightMemoryResponse(BaseModel):
    """Response from storing analyst feedback."""
    memory_id: str = Field(description="Created hindsight memory ID")
    feedback_type: str = Field(description="Feedback type stored")
    message: str = Field(description="Confirmation message")


class SimilarCasesContext(BaseModel):
    """Context from similar past cases to inform current investigation."""
    similar_cases: list[dict] = Field(description="List of similar past cases with feedback")
    accuracy_rate: float = Field(ge=0, le=100, description="Accuracy rate from past feedback")
    common_patterns: list[str] = Field(description="Common patterns from similar cases")


class RiskScoreRequest(BaseModel):
    """XGBoost-based fraud risk scoring request."""
    amount: float = Field(gt=0, description="Transaction amount in USD")
    merchant_category: str = Field(min_length=1, max_length=100, description="Merchant category code")
    transaction_type: str = Field(description="Type of transaction (online, atm, pos, etc.)")
    time_of_day: int = Field(ge=0, le=23, description="Hour of transaction (0-23)")
    days_since_account_opened: int = Field(ge=0, description="Days since account opened")
    transaction_count_today: int = Field(ge=0, description="Number of transactions today")
    location_mismatch: bool = Field(description="True if transaction location differs from usual")
    velocity_score: float = Field(ge=0, le=100, description="Transaction velocity score (0-100)")


class RiskScoreResponse(BaseModel):
    """XGBoost fraud risk score response."""
    risk_score: float = Field(ge=0, le=100, description="Fraud risk score (0-100)")
    risk_category: str = Field(description="Risk category: CRITICAL, HIGH, MEDIUM, LOW")
    confidence: float = Field(ge=0, le=100, description="Model confidence (0-100)")
    feature_importance: dict = Field(description="Top contributing features")
    timestamp: str = Field(description="ISO format timestamp")


class BatchRiskScoreRequest(BaseModel):
    """Batch scoring request for multiple transactions."""
    transactions: list[RiskScoreRequest] = Field(description="List of transactions to score")


class BatchRiskScoreResponse(BaseModel):
    """Batch risk score response."""
    scores: list[RiskScoreResponse] = Field(description="Risk scores for each transaction")
    summary: dict = Field(description="Summary statistics (avg_risk, critical_count, etc.)")

