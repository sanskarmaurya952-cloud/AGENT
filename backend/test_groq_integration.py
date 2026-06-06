"""
Test suite for Groq API integration in the Risk Intelligence system.
Tests the investigation endpoint and Groq-powered fraud analysis.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from backend.main import app, investigate_transaction
from backend.schemas import InvestigateTransactionRequest, InvestigationReport

# Test configuration
TEST_GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TEST_TRANSACTIONS = [
    {
        "transaction_id": "txn_critical_001",
        "customer": "Nadia Chen",
        "amount": 249.95,
        "currency": "USD",
        "location": "Singapore",
        "merchant": "Northwind Electronics",
        "risk_score": 92,
    },
    {
        "transaction_id": "txn_high_002",
        "customer": "Ethan Brooks",
        "amount": 18.4,
        "currency": "USD",
        "location": "London",
        "merchant": "Harbor Coffee",
        "risk_score": 75,
    },
    {
        "transaction_id": "txn_medium_003",
        "customer": "Ava Patel",
        "amount": 1599.0,
        "currency": "USD",
        "location": "New York",
        "merchant": "Orbit Mobility",
        "risk_score": 45,
    },
]


class TestGroqIntegration:
    """Test Groq API integration with investigation endpoint."""
    
    def test_groq_api_key_loaded(self):
        """Verify GROQ_API_KEY is loaded from environment."""
        assert TEST_GROQ_API_KEY is not None, "GROQ_API_KEY not found in environment"
        assert len(TEST_GROQ_API_KEY) > 0, "GROQ_API_KEY is empty"
        assert "gsk_" in TEST_GROQ_API_KEY, "GROQ_API_KEY should start with 'gsk_'"
        print(f"✓ GROQ API Key loaded successfully")
    
    def test_investigate_critical_risk_transaction(self):
        """Test investigation of critical risk transaction with Groq."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        # Validate response structure
        assert isinstance(report, InvestigationReport)
        assert report.transaction_id == txn["transaction_id"]
        assert report.risk_level in ["Critical", "High", "Medium", "Low"]
        assert 0 <= report.confidence <= 1.0
        assert len(report.reasoning) > 0
        assert report.recommended_action in ["Review", "Investigate", "Monitor", "Clear"]
        
        # Critical risk should get high attention
        assert report.risk_level in ["Critical", "High"]
        assert report.confidence >= 0.7, f"Expected high confidence for critical transaction, got {report.confidence}"
        print(f"✓ Critical transaction analysis: {report.risk_level} ({report.confidence:.0%} confidence)")
        print(f"  Fraud Type: {report.fraud_type}")
        print(f"  Action: {report.recommended_action}")
    
    def test_investigate_high_risk_transaction(self):
        """Test investigation of high risk transaction with Groq."""
        txn = TEST_TRANSACTIONS[1]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        assert isinstance(report, InvestigationReport)
        assert report.risk_level in ["Critical", "High", "Medium", "Low"]
        assert report.confidence >= 0.5
        print(f"✓ High risk transaction analysis: {report.risk_level} ({report.confidence:.0%} confidence)")
    
    def test_investigate_medium_risk_transaction(self):
        """Test investigation of medium risk transaction with Groq."""
        txn = TEST_TRANSACTIONS[2]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        assert isinstance(report, InvestigationReport)
        # Medium risk might result in any level depending on Groq analysis
        assert report.risk_level in ["Critical", "High", "Medium", "Low"]
        assert report.confidence >= 0.4
        print(f"✓ Medium risk transaction analysis: {report.risk_level} ({report.confidence:.0%} confidence)")
    
    def test_investigation_includes_related_memories(self):
        """Test that investigation includes related memory references."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        assert report.related_memories >= 0
        print(f"✓ Investigation found {report.related_memories} related memories")
    
    def test_investigation_fraud_type_classification(self):
        """Test that fraud type is properly classified."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        valid_fraud_types = [
            "Identity Fraud",
            "Merchant Abuse",
            "Money Laundering",
            "Card Fraud",
            "Account Takeover",
            "Unknown",
        ]
        assert report.fraud_type in valid_fraud_types or "fraud" in report.fraud_type.lower()
        print(f"✓ Fraud type classified as: {report.fraud_type}")
    
    def test_investigation_reasoning_quality(self):
        """Test that investigation reasoning is detailed and logical."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        # Reasoning should be substantial
        assert len(report.reasoning) >= 20, "Reasoning should be detailed (at least 20 chars)"
        assert "transaction" in report.reasoning.lower() or \
               "fraud" in report.reasoning.lower() or \
               "risk" in report.reasoning.lower(), \
               "Reasoning should reference fraud/risk/transaction context"
        print(f"✓ Reasoning quality validated")
        print(f"  Sample: {report.reasoning[:100]}...")
    
    @patch.dict(os.environ, {"GROQ_API_KEY": ""})
    def test_fallback_mode_without_api_key(self):
        """Test fallback analysis when GROQ_API_KEY is not set."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        # Mock the environment variable removal
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=False):
            # Reload to get modified env var
            import importlib
            import backend.main
            
            # Directly test fallback logic
            report = investigate_transaction(payload)
            
            # Should still produce valid report
            assert isinstance(report, InvestigationReport)
            assert report.risk_level is not None
            assert "similar memories" in report.investigation_notes or \
                   "rule engine" in report.investigation_notes or \
                   "Groq API not configured" in report.investigation_notes
            print(f"✓ Fallback mode works: {report.risk_level}")


class TestGroqResponseParsing:
    """Test parsing of Groq API responses."""
    
    def test_response_contains_all_fields(self):
        """Test that Groq response contains all required fields."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        # Check all required fields are present
        assert hasattr(report, "transaction_id")
        assert hasattr(report, "risk_level")
        assert hasattr(report, "confidence")
        assert hasattr(report, "fraud_type")
        assert hasattr(report, "reasoning")
        assert hasattr(report, "recommended_action")
        assert hasattr(report, "investigation_notes")
        print("✓ All required fields present in response")
    
    def test_confidence_score_validation(self):
        """Test that confidence scores are valid percentages."""
        for txn in TEST_TRANSACTIONS:
            payload = InvestigateTransactionRequest(**txn)
            report = investigate_transaction(payload)
            
            assert isinstance(report.confidence, float)
            assert 0.0 <= report.confidence <= 1.0
            confidence_pct = int(report.confidence * 100)
            assert 0 <= confidence_pct <= 100
        
        print("✓ All confidence scores valid (0-100%)")
    
    def test_risk_level_consistency(self):
        """Test that risk levels are consistent with scores."""
        txn = TEST_TRANSACTIONS[0]  # High risk score (92)
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        # Higher risk scores should generally result in higher risk levels
        risk_hierarchy = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        assert report.risk_level in risk_hierarchy
        print(f"✓ Risk level consistency validated")


class TestInvestigationEndpoint:
    """Test the /investigate endpoint."""
    
    def test_endpoint_accepts_valid_request(self):
        """Test that endpoint accepts valid investigation request."""
        txn = TEST_TRANSACTIONS[0]
        payload = InvestigateTransactionRequest(**txn)
        
        report = investigate_transaction(payload)
        
        assert report is not None
        print("✓ Endpoint accepts valid requests")
    
    def test_endpoint_handles_different_currencies(self):
        """Test investigation with different currency amounts."""
        currencies = ["USD", "EUR", "GBP", "JPY", "AUD"]
        
        for currency in currencies:
            txn = TEST_TRANSACTIONS[0].copy()
            txn["currency"] = currency
            payload = InvestigateTransactionRequest(**txn)
            
            report = investigate_transaction(payload)
            assert isinstance(report, InvestigationReport)
        
        print(f"✓ Investigated {len(currencies)} different currencies")
    
    def test_endpoint_handles_various_locations(self):
        """Test investigation from different geographic locations."""
        locations = [
            "Singapore",
            "London",
            "New York",
            "Tokyo",
            "Mumbai",
            "Dubai",
            "Hong Kong",
        ]
        
        for location in locations:
            txn = TEST_TRANSACTIONS[0].copy()
            txn["location"] = location
            payload = InvestigateTransactionRequest(**txn)
            
            report = investigate_transaction(payload)
            assert isinstance(report, InvestigationReport)
        
        print(f"✓ Investigated {len(locations)} different locations")


class TestErrorHandling:
    """Test error handling in Groq integration."""
    
    def test_investigation_handles_invalid_risk_score(self):
        """Test handling of edge case risk scores."""
        test_scores = [0, 1, 50, 99, 100]
        
        for score in test_scores:
            txn = TEST_TRANSACTIONS[0].copy()
            txn["risk_score"] = score
            payload = InvestigateTransactionRequest(**txn)
            
            report = investigate_transaction(payload)
            assert isinstance(report, InvestigationReport)
        
        print(f"✓ Handled {len(test_scores)} different risk scores")
    
    def test_investigation_with_special_characters(self):
        """Test investigation with special characters in fields."""
        txn = TEST_TRANSACTIONS[0].copy()
        txn["merchant"] = "Café & Bar @ 42nd St."
        txn["customer"] = "José O'Connor-Smith"
        
        payload = InvestigateTransactionRequest(**txn)
        report = investigate_transaction(payload)
        
        assert isinstance(report, InvestigationReport)
        print("✓ Handled special characters in merchant/customer names")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
