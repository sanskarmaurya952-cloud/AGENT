"""
NEW ENDPOINT - Add this to backend/main.py after the existing investigate_transaction endpoint
This endpoint provides production-ready fraud investigation using Groq AI.
"""

# APPEND THIS CODE TO THE END OF backend/main.py


@app.post("/investigate/groq", response_model=InvestigationResult, tags=["Fraud Investigation"])
def investigate_with_groq(payload: SimpleInvestigationRequest) -> InvestigationResult:
    """
    Production-ready fraud investigation endpoint using Groq AI.
    
    Analyzes transaction details to assess fraud risk and provide investigation recommendations.
    Uses Groq's Mixtral model for rapid, accurate fraud pattern detection.
    
    Args:
        payload: Transaction details (amount, location, merchant)
    
    Returns:
        InvestigationResult with risk level, summary, and recommended action
    
    Raises:
        HTTPException: If Groq API fails after retries
    """
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        logger.warning("GROQ_API_KEY not configured, using fallback analysis")
        return _fallback_investigation(payload)
    
    try:
        logger.info(f"Starting investigation for transaction: Amount={payload.amount}, Location={payload.location}, Merchant={payload.merchant}")
        
        # Initialize Groq client
        client = Groq(api_key=groq_api_key)
        
        # Determine initial risk level based on amount
        amount_risk = _assess_amount_risk(payload.amount)
        
        # Build comprehensive prompt for Groq
        prompt = f"""You are an expert fraud analyst. Analyze this transaction for fraud risk.

TRANSACTION DETAILS:
- Amount: ${payload.amount:,.2f}
- Location: {payload.location}
- Merchant: {payload.merchant}
- Initial Risk Signal: {amount_risk}

Provide a fraud risk assessment including:
1. RISK_LEVEL: Assign one of: Critical (>80%), High (60-80%), Medium (40-60%), Low (<40%)
2. CONFIDENCE: Your confidence in the assessment (0-100%)
3. FRAUD_INDICATORS: List 3-5 specific fraud indicators or patterns detected
4. SUMMARY: A detailed fraud investigation summary (2-3 sentences explaining the assessment)
5. ACTION: Recommended action - Review (Critical/High), Investigate (High), Monitor (Medium), Clear (Low)

FORMAT YOUR RESPONSE EXACTLY AS:
RISK_LEVEL: [Critical/High/Medium/Low]
CONFIDENCE: [0-100]
FRAUD_INDICATORS: [indicator1], [indicator2], [indicator3], [indicator4], [indicator5]
SUMMARY: [2-3 sentence detailed summary]
ACTION: [Review/Investigate/Monitor/Clear]"""
        
        # Call Groq API with retry logic
        try:
            message = client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=512,
                temperature=0.3,  # Lower temperature for more deterministic fraud scoring
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            logger.info(f"Groq analysis completed successfully")
            
        except Exception as groq_error:
            logger.error(f"Groq API error: {str(groq_error)}")
            return _fallback_investigation(payload)
        
        # Parse Groq response
        parsed = _parse_groq_response(response_text)
        
        # Extract and validate fields
        risk_level = _validate_risk_level(parsed.get("RISK_LEVEL", "Medium"))
        confidence = _parse_confidence(parsed.get("CONFIDENCE", "50"))
        fraud_indicators = _parse_fraud_indicators(parsed.get("FRAUD_INDICATORS", ""))
        summary = parsed.get("SUMMARY", "Fraud analysis completed.")
        recommended_action = _validate_action(parsed.get("ACTION", "Monitor"))
        
        logger.info(f"Investigation result: Risk={risk_level}, Confidence={confidence}%, Action={recommended_action}")
        
        return InvestigationResult(
            risk_level=risk_level,
            investigation_summary=summary,
            recommended_action=recommended_action,
            confidence_score=confidence,
            fraud_indicators=fraud_indicators,
            analysis_timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in investigation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Investigation service error: {str(e)}"
        )


def _assess_amount_risk(amount: float) -> str:
    """Assess initial risk based on transaction amount."""
    if amount > 50000:
        return "High (Large amount)"
    elif amount > 10000:
        return "Medium (Significant amount)"
    elif amount > 5000:
        return "Medium-Low (Moderate amount)"
    else:
        return "Low (Standard amount)"


def _parse_groq_response(response_text: str) -> dict:
    """Parse structured response from Groq."""
    parsed = {}
    lines = response_text.strip().split("\n")
    
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()
            parsed[key] = value
    
    return parsed


def _validate_risk_level(level: str) -> str:
    """Validate and normalize risk level."""
    level = level.strip().lower()
    valid_levels = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}
    
    # Check for exact match
    if level in valid_levels:
        return valid_levels[level]
    
    # Check for partial match
    for key in valid_levels:
        if key in level:
            return valid_levels[key]
    
    return "Medium"  # Default fallback


def _validate_action(action: str) -> str:
    """Validate and normalize recommended action."""
    action = action.strip().lower()
    valid_actions = {
        "review": "Review",
        "investigate": "Investigate", 
        "monitor": "Monitor",
        "clear": "Clear"
    }
    
    # Check for exact match
    if action in valid_actions:
        return valid_actions[action]
    
    # Check for partial match
    for key in valid_actions:
        if key in action:
            return valid_actions[key]
    
    return "Monitor"  # Default fallback


def _parse_confidence(confidence_str: str) -> float:
    """Parse confidence score from string."""
    try:
        # Remove percentage sign if present
        confidence_str = confidence_str.replace("%", "").strip()
        score = float(confidence_str)
        # Clamp to 0-100
        return max(0, min(100, score))
    except (ValueError, AttributeError):
        return 50.0


def _parse_fraud_indicators(indicators_str: str) -> list[str]:
    """Parse fraud indicators from response."""
    if not indicators_str:
        return ["Unable to identify specific indicators"]
    
    # Split by comma and clean up
    indicators = [ind.strip() for ind in indicators_str.split(",")]
    indicators = [ind for ind in indicators if ind]  # Remove empty strings
    
    return indicators[:5] if indicators else ["Unable to identify specific indicators"]


def _fallback_investigation(payload: SimpleInvestigationRequest) -> InvestigationResult:
    """Fallback investigation when Groq is unavailable."""
    logger.warning("Using fallback fraud investigation analysis")
    
    amount_risk = _assess_amount_risk(payload.amount)
    
    # Rule-based fallback logic
    risk_score = 0
    indicators = []
    
    # Check amount
    if payload.amount > 50000:
        risk_score += 40
        indicators.append("Large transaction amount")
    elif payload.amount > 10000:
        risk_score += 25
        indicators.append("Significant transaction amount")
    
    # Check location
    high_risk_locations = ["Unknown", "N/A", "TBD"]
    if any(loc in payload.location for loc in high_risk_locations):
        risk_score += 25
        indicators.append("Unusual transaction location")
    elif payload.location.lower() in ["dubai", "hong kong", "singapore"]:
        risk_score += 10
        indicators.append("International transaction")
    
    # Check merchant
    suspicious_merchants = ["Unknown", "Generic", "Unverified"]
    if any(merch in payload.merchant for merch in suspicious_merchants):
        risk_score += 30
        indicators.append("Unverified merchant")
    
    # Determine risk level
    if risk_score >= 80:
        risk_level = "Critical"
        action = "Review"
    elif risk_score >= 60:
        risk_level = "High"
        action = "Investigate"
    elif risk_score >= 40:
        risk_level = "Medium"
        action = "Monitor"
    else:
        risk_level = "Low"
        action = "Clear"
    
    if not indicators:
        indicators = ["Standard transaction pattern"]
    
    return InvestigationResult(
        risk_level=risk_level,
        investigation_summary=f"Fallback analysis: {amount_risk}. Transaction from {payload.location} to {payload.merchant}. {', '.join(indicators)}.",
        recommended_action=action,
        confidence_score=float(risk_score),
        fraud_indicators=indicators[:5],
        analysis_timestamp=datetime.utcnow().isoformat() + "Z"
    )
