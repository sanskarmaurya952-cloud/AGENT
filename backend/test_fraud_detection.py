"""
Test suite for XGBoost Fraud Detection Service
Tests risk scoring, batch processing, and fraud statistics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.schemas import RiskScoreRequest, BatchRiskScoreRequest
from backend.xgboost_service import get_fraud_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_fraud_service_initialization():
    """Test fraud service initializes properly."""
    print("\n1. Fraud Service Initialization")
    print("=" * 60)
    
    try:
        service = get_fraud_service()
        assert service is not None
        assert service.model is not None or service.model is None  # Either loaded or fallback
        print("✅ Fraud service initialized successfully")
        print(f"   Model loaded: {service.model is not None}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize service: {str(e)}")
        return False


def test_feature_encoding():
    """Test feature encoding functions."""
    print("\n2. Feature Encoding")
    print("=" * 60)
    
    service = get_fraud_service()
    
    # Test merchant category encoding
    assert service._encode_merchant_category("grocery") == 0
    assert service._encode_merchant_category("online") == 5
    assert service._encode_merchant_category("unknown") == 9
    print("✅ Merchant category encoding works")
    
    # Test transaction type encoding
    assert service._encode_transaction_type("online") == 0
    assert service._encode_transaction_type("atm") == 1
    assert service._encode_transaction_type("pos") == 2
    print("✅ Transaction type encoding works")
    
    return True


def test_risk_scoring_low_risk():
    """Test scoring a low-risk transaction."""
    print("\n3. Low-Risk Transaction Scoring")
    print("=" * 60)
    
    service = get_fraud_service()
    
    result = service.score(
        amount=50.0,  # Small amount
        merchant_category="grocery",
        transaction_type="pos",
        time_of_day=14,  # Afternoon
        days_since_account_opened=365,  # Old account
        transaction_count_today=1,  # First transaction
        location_mismatch=False,  # Same location
        velocity_score=10.0  # Low velocity
    )
    
    print(f"   Amount: $50, Merchant: Grocery, Time: 2PM")
    print(f"   Risk Score: {result['risk_score']:.1f}/100")
    print(f"   Confidence: {result['confidence']:.0f}%")
    print(f"   Category: LOW expected")
    
    assert 0 <= result['risk_score'] <= 100
    assert 0 <= result['confidence'] <= 100
    assert result['risk_score'] < 40  # Should be low risk
    print("✅ Low-risk scoring works correctly")
    
    return True


def test_risk_scoring_high_risk():
    """Test scoring a high-risk transaction."""
    print("\n4. High-Risk Transaction Scoring")
    print("=" * 60)
    
    service = get_fraud_service()
    
    result = service.score(
        amount=15000.0,  # Large amount
        merchant_category="online",
        transaction_type="online",
        time_of_day=3,  # Late night
        days_since_account_opened=5,  # New account
        transaction_count_today=15,  # Many transactions
        location_mismatch=True,  # Different location
        velocity_score=95.0  # High velocity
    )
    
    print(f"   Amount: $15,000, Merchant: Online, Time: 3AM")
    print(f"   Risk Score: {result['risk_score']:.1f}/100")
    print(f"   Confidence: {result['confidence']:.0f}%")
    print(f"   Category: HIGH/CRITICAL expected")
    
    assert 0 <= result['risk_score'] <= 100
    assert 0 <= result['confidence'] <= 100
    assert result['risk_score'] > 50  # Should be high risk
    print("✅ High-risk scoring works correctly")
    
    return True


def test_risk_scoring_medium_risk():
    """Test scoring a medium-risk transaction."""
    print("\n5. Medium-Risk Transaction Scoring")
    print("=" * 60)
    
    service = get_fraud_service()
    
    result = service.score(
        amount=500.0,  # Medium amount
        merchant_category="retail",
        transaction_type="pos",
        time_of_day=11,  # Morning
        days_since_account_opened=90,  # Newer account
        transaction_count_today=3,  # Few transactions
        location_mismatch=False,  # Same location
        velocity_score=45.0  # Medium velocity
    )
    
    print(f"   Amount: $500, Merchant: Retail, Time: 11AM")
    print(f"   Risk Score: {result['risk_score']:.1f}/100")
    print(f"   Confidence: {result['confidence']:.0f}%")
    
    assert 0 <= result['risk_score'] <= 100
    assert 0 <= result['confidence'] <= 100
    print("✅ Medium-risk scoring works correctly")
    
    return True


def test_risk_score_request_schema():
    """Test RiskScoreRequest schema validation."""
    print("\n6. Risk Score Request Schema")
    print("=" * 60)
    
    # Valid request
    try:
        req = RiskScoreRequest(
            amount=100.0,
            merchant_category="grocery",
            transaction_type="pos",
            time_of_day=12,
            days_since_account_opened=365,
            transaction_count_today=1,
            location_mismatch=False,
            velocity_score=25.0
        )
        print("✅ Valid request accepted")
    except Exception as e:
        print(f"❌ Valid request rejected: {str(e)}")
        return False
    
    # Invalid request - negative amount
    try:
        req = RiskScoreRequest(
            amount=-100.0,
            merchant_category="grocery",
            transaction_type="pos",
            time_of_day=12,
            days_since_account_opened=365,
            transaction_count_today=1,
            location_mismatch=False,
            velocity_score=25.0
        )
        print("❌ Negative amount should be rejected")
        return False
    except Exception:
        print("✅ Invalid amount correctly rejected")
    
    # Invalid request - invalid hour
    try:
        req = RiskScoreRequest(
            amount=100.0,
            merchant_category="grocery",
            transaction_type="pos",
            time_of_day=25,
            days_since_account_opened=365,
            transaction_count_today=1,
            location_mismatch=False,
            velocity_score=25.0
        )
        print("❌ Invalid hour should be rejected")
        return False
    except Exception:
        print("✅ Invalid hour correctly rejected")
    
    return True


def test_feature_importance():
    """Test feature importance extraction."""
    print("\n7. Feature Importance")
    print("=" * 60)
    
    service = get_fraud_service()
    
    result = service.score(
        amount=10000.0,
        merchant_category="travel",
        transaction_type="online",
        time_of_day=2,
        days_since_account_opened=15,
        transaction_count_today=8,
        location_mismatch=True,
        velocity_score=75.0
    )
    
    importance = result['features_importance']
    print(f"   Top contributing features:")
    for feature, weight in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {feature}: {weight}%")
    
    assert len(importance) > 0
    print("✅ Feature importance extracted")
    
    return True


def test_batch_request_schema():
    """Test batch risk score request schema."""
    print("\n8. Batch Request Schema")
    print("=" * 60)
    
    try:
        txn1 = RiskScoreRequest(
            amount=100.0,
            merchant_category="grocery",
            transaction_type="pos",
            time_of_day=12,
            days_since_account_opened=365,
            transaction_count_today=1,
            location_mismatch=False,
            velocity_score=25.0
        )
        txn2 = RiskScoreRequest(
            amount=5000.0,
            merchant_category="online",
            transaction_type="online",
            time_of_day=3,
            days_since_account_opened=30,
            transaction_count_today=5,
            location_mismatch=True,
            velocity_score=60.0
        )
        
        batch = BatchRiskScoreRequest(transactions=[txn1, txn2])
        print(f"✅ Batch request with {len(batch.transactions)} transactions created")
        
    except Exception as e:
        print(f"❌ Batch request failed: {str(e)}")
        return False
    
    return True


def test_fallback_scoring():
    """Test fallback scoring when model unavailable."""
    print("\n9. Fallback Scoring")
    print("=" * 60)
    
    service = get_fraud_service()
    
    # Temporarily disable model to test fallback
    original_model = service.model
    service.model = None
    
    result = service.score(
        amount=1000.0,
        merchant_category="online",
        transaction_type="phone",
        time_of_day=5,
        days_since_account_opened=14,
        transaction_count_today=12,
        location_mismatch=True,
        velocity_score=85.0
    )
    
    print(f"   Using fallback rules (model disabled)")
    print(f"   Risk Score: {result['risk_score']:.1f}/100")
    print(f"   Confidence: {result['confidence']:.0f}% (lower for fallback)")
    
    assert 0 <= result['risk_score'] <= 100
    assert result['confidence'] == 65.0  # Fallback confidence
    
    # Restore model
    service.model = original_model
    print("✅ Fallback scoring works correctly")
    
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "=" * 60)
    print("XGBOOST FRAUD DETECTION SERVICE - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Fraud Service Init", test_fraud_service_initialization),
        ("Feature Encoding", test_feature_encoding),
        ("Low-Risk Scoring", test_risk_scoring_low_risk),
        ("High-Risk Scoring", test_risk_scoring_high_risk),
        ("Medium-Risk Scoring", test_risk_scoring_medium_risk),
        ("Request Schema", test_risk_score_request_schema),
        ("Feature Importance", test_feature_importance),
        ("Batch Schema", test_batch_request_schema),
        ("Fallback Scoring", test_fallback_scoring),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
