"""
Test script for the production-ready POST /investigate/groq endpoint.
Tests the new simplified fraud investigation endpoint with Groq AI.
"""

import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8000"
INVESTIGATE_ENDPOINT = f"{API_URL}/investigate/groq"

# Test cases
TEST_CASES = [
    {
        "name": "High-value Dubai transaction",
        "payload": {
            "amount": 50000,
            "location": "Dubai",
            "merchant": "Unknown Merchant"
        },
        "expected_risk": "High"
    },
    {
        "name": "Large international transaction",
        "payload": {
            "amount": 75000,
            "location": "Hong Kong",
            "merchant": "Unverified Trading LLC"
        },
        "expected_risk": "Critical"
    },
    {
        "name": "Moderate domestic transaction",
        "payload": {
            "amount": 2500,
            "location": "New York",
            "merchant": "Amazon"
        },
        "expected_risk": "Low"
    },
    {
        "name": "Suspicious crypto exchange",
        "payload": {
            "amount": 35000,
            "location": "N/A",
            "merchant": "Unknown"
        },
        "expected_risk": "High"
    },
]


def test_endpoint():
    """Test the /investigate/groq endpoint with various payloads."""
    print("=" * 80)
    print("PRODUCTION-READY GROQ FRAUD INVESTIGATION ENDPOINT TEST")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"  Payload: {json.dumps(test_case['payload'], indent=2)}")
        print()
        
        try:
            # Make request
            response = requests.post(
                INVESTIGATE_ENDPOINT,
                json=test_case['payload'],
                timeout=30
            )
            
            # Check status code
            if response.status_code != 200:
                print(f"  ❌ FAILED: Expected status 200, got {response.status_code}")
                print(f"  Response: {response.text}")
                failed += 1
                print()
                continue
            
            # Parse response
            data = response.json()
            
            # Validate response structure
            required_fields = [
                "risk_level",
                "investigation_summary",
                "recommended_action",
                "confidence_score",
                "fraud_indicators",
                "analysis_timestamp"
            ]
            
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                print(f"  ❌ FAILED: Missing fields: {missing_fields}")
                failed += 1
                print()
                continue
            
            # Validate field types and values
            risk_level = data["risk_level"]
            valid_risks = ["Critical", "High", "Medium", "Low"]
            if risk_level not in valid_risks:
                print(f"  ❌ FAILED: Invalid risk level: {risk_level}")
                failed += 1
                print()
                continue
            
            action = data["recommended_action"]
            valid_actions = ["Review", "Investigate", "Monitor", "Clear"]
            if action not in valid_actions:
                print(f"  ❌ FAILED: Invalid action: {action}")
                failed += 1
                print()
                continue
            
            confidence = data["confidence_score"]
            if not (0 <= confidence <= 100):
                print(f"  ❌ FAILED: Confidence out of range: {confidence}")
                failed += 1
                print()
                continue
            
            indicators = data["fraud_indicators"]
            if not isinstance(indicators, list) or len(indicators) == 0:
                print(f"  ❌ FAILED: Invalid fraud indicators: {indicators}")
                failed += 1
                print()
                continue
            
            # Print response
            print(f"  ✅ PASSED")
            print(f"  Risk Level: {risk_level}")
            print(f"  Confidence: {confidence:.0f}%")
            print(f"  Recommended Action: {action}")
            print(f"  Summary: {data['investigation_summary']}")
            print(f"  Fraud Indicators: {', '.join(indicators[:3])}...")
            print(f"  Analysis Timestamp: {data['analysis_timestamp']}")
            passed += 1
            print()
            
        except requests.exceptions.ConnectionError:
            print(f"  ❌ FAILED: Cannot connect to API at {API_URL}")
            print(f"     Make sure the backend is running on port 8000")
            failed += 1
            print()
        except Exception as e:
            print(f"  ❌ FAILED: {str(e)}")
            failed += 1
            print()
    
    # Summary
    print("=" * 80)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print("=" * 80)
    
    return failed == 0


def test_error_handling():
    """Test error handling for invalid inputs."""
    print()
    print("=" * 80)
    print("ERROR HANDLING TEST")
    print("=" * 80)
    print()
    
    error_cases = [
        {
            "name": "Missing amount field",
            "payload": {
                "location": "Dubai",
                "merchant": "Unknown Merchant"
            }
        },
        {
            "name": "Invalid amount (negative)",
            "payload": {
                "amount": -1000,
                "location": "Dubai",
                "merchant": "Unknown Merchant"
            }
        },
        {
            "name": "Empty merchant name",
            "payload": {
                "amount": 50000,
                "location": "Dubai",
                "merchant": ""
            }
        },
    ]
    
    for test_case in error_cases:
        print(f"Test: {test_case['name']}")
        print(f"  Payload: {json.dumps(test_case['payload'])}")
        
        try:
            response = requests.post(
                INVESTIGATE_ENDPOINT,
                json=test_case['payload'],
                timeout=30
            )
            
            # Should get 422 Unprocessable Entity for validation errors
            if response.status_code in [400, 422]:
                print(f"  ✅ PASSED: Correctly rejected with status {response.status_code}")
            else:
                print(f"  ❌ UNEXPECTED: Got status {response.status_code}")
            print()
            
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Cannot connect to API")
            print()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            print()


if __name__ == "__main__":
    print()
    print("Testing POST /investigate/groq - Production-Ready Fraud Investigation Endpoint")
    print()
    
    # Run tests
    success = test_endpoint()
    test_error_handling()
    
    print()
    if success:
        print("✅ All tests passed! Endpoint is production-ready.")
    else:
        print("⚠️  Some tests failed. Check the endpoint implementation.")
