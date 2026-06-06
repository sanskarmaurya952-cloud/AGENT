"""
Test suite for Risk Intelligence API endpoints.
Tests FastAPI routes with Groq-powered investigation.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestDashboardEndpoint:
    """Test /dashboard endpoint."""
    
    def test_dashboard_returns_200(self):
        """Test dashboard endpoint returns successful response."""
        response = client.get("/dashboard")
        assert response.status_code == 200
        print("✓ Dashboard endpoint returns 200 OK")
    
    def test_dashboard_contains_kpis(self):
        """Test dashboard includes KPI data."""
        response = client.get("/dashboard")
        data = response.json()
        
        assert "kpis" in data
        assert len(data["kpis"]) == 4
        print(f"✓ Dashboard contains {len(data['kpis'])} KPIs")
    
    def test_dashboard_contains_summary(self):
        """Test dashboard includes summary statistics."""
        response = client.get("/dashboard")
        data = response.json()
        
        assert "summary" in data
        assert "totalTransactions" in data["summary"]
        print("✓ Dashboard contains summary statistics")
    
    def test_dashboard_contains_memory_cards(self):
        """Test dashboard includes memory cards."""
        response = client.get("/dashboard")
        data = response.json()
        
        assert "memoryCards" in data
        print(f"✓ Dashboard contains {len(data.get('memoryCards', []))} memory cards")


class TestTransactionsEndpoint:
    """Test /transactions endpoint."""
    
    def test_transactions_returns_200(self):
        """Test transactions endpoint returns successful response."""
        response = client.get("/transactions")
        assert response.status_code == 200
        print("✓ Transactions endpoint returns 200 OK")
    
    def test_transactions_contains_items(self):
        """Test transactions response includes items."""
        response = client.get("/transactions")
        data = response.json()
        
        assert "items" in data
        assert isinstance(data["items"], list)
        print(f"✓ Transactions endpoint returns {len(data['items'])} items")
    
    def test_transaction_item_structure(self):
        """Test individual transaction item has required fields."""
        response = client.get("/transactions")
        data = response.json()
        
        if data["items"]:
            txn = data["items"][0]
            required_fields = ["id", "customer", "amount", "currency", "location", 
                             "merchant", "risk", "status", "action", "riskScore"]
            
            for field in required_fields:
                assert field in txn, f"Missing field: {field}"
            
            print(f"✓ Transaction item has all required fields")
    
    def test_transactions_pagination_info(self):
        """Test transactions response includes pagination info."""
        response = client.get("/transactions")
        data = response.json()
        
        assert "page" in data
        assert "pageSize" in data
        assert "total" in data
        print(f"✓ Transactions pagination: Page {data['page']}, Size {data['pageSize']}, Total {data['total']}")


class TestAlertsEndpoint:
    """Test /alerts endpoint."""
    
    def test_alerts_returns_200(self):
        """Test alerts endpoint returns successful response."""
        response = client.get("/alerts")
        assert response.status_code == 200
        print("✓ Alerts endpoint returns 200 OK")
    
    def test_alerts_contains_items(self):
        """Test alerts response includes items."""
        response = client.get("/alerts")
        data = response.json()
        
        assert "items" in data
        assert isinstance(data["items"], list)
        print(f"✓ Alerts endpoint returns {len(data['items'])} items")
    
    def test_alert_item_structure(self):
        """Test individual alert item has required fields."""
        response = client.get("/alerts")
        data = response.json()
        
        if data["items"]:
            alert = data["items"][0]
            required_fields = ["id", "type", "severity", "message", "status", "time"]
            
            for field in required_fields:
                assert field in alert, f"Missing field: {field}"
            
            print(f"✓ Alert item has all required fields")


class TestInvestigateEndpoint:
    """Test /investigate endpoint with Groq AI."""
    
    def test_investigate_returns_200(self):
        """Test investigation endpoint returns successful response."""
        payload = {
            "transaction_id": "txn_test_001",
            "customer": "Test Customer",
            "amount": 500.0,
            "currency": "USD",
            "location": "Test City",
            "merchant": "Test Merchant",
            "risk_score": 75,
        }
        
        response = client.post("/investigate", json=payload)
        assert response.status_code == 200
        print("✓ Investigation endpoint returns 200 OK")
    
    def test_investigate_response_structure(self):
        """Test investigation response has required fields."""
        payload = {
            "transaction_id": "txn_test_002",
            "customer": "Test Customer",
            "amount": 500.0,
            "currency": "USD",
            "location": "Test City",
            "merchant": "Test Merchant",
            "risk_score": 80,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        required_fields = [
            "transaction_id",
            "risk_level",
            "confidence",
            "fraud_type",
            "reasoning",
            "related_memories",
            "recommended_action",
            "investigation_notes",
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        print("✓ Investigation response has all required fields")
    
    def test_investigate_critical_transaction(self):
        """Test investigation of critical risk transaction."""
        payload = {
            "transaction_id": "txn_critical_001",
            "customer": "Nadia Chen",
            "amount": 249.95,
            "currency": "USD",
            "location": "Singapore",
            "merchant": "Northwind Electronics",
            "risk_score": 92,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        assert data["risk_level"] in ["Critical", "High", "Medium", "Low"]
        assert 0 <= data["confidence"] <= 1.0
        print(f"✓ Critical transaction investigation: {data['risk_level']} ({int(data['confidence']*100)}% confidence)")
    
    def test_investigate_high_transaction(self):
        """Test investigation of high risk transaction."""
        payload = {
            "transaction_id": "txn_high_001",
            "customer": "Ethan Brooks",
            "amount": 18.4,
            "currency": "USD",
            "location": "London",
            "merchant": "Harbor Coffee",
            "risk_score": 75,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        assert data["risk_level"] in ["Critical", "High", "Medium", "Low"]
        print(f"✓ High risk transaction investigation: {data['risk_level']}")
    
    def test_investigate_medium_transaction(self):
        """Test investigation of medium risk transaction."""
        payload = {
            "transaction_id": "txn_medium_001",
            "customer": "Ava Patel",
            "amount": 1599.0,
            "currency": "USD",
            "location": "New York",
            "merchant": "Orbit Mobility",
            "risk_score": 45,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        assert data["risk_level"] in ["Critical", "High", "Medium", "Low"]
        print(f"✓ Medium risk transaction investigation: {data['risk_level']}")
    
    def test_investigate_low_transaction(self):
        """Test investigation of low risk transaction."""
        payload = {
            "transaction_id": "txn_low_001",
            "customer": "Jane Doe",
            "amount": 25.0,
            "currency": "USD",
            "location": "Seattle",
            "merchant": "Local Café",
            "risk_score": 15,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        assert data["risk_level"] in ["Critical", "High", "Medium", "Low"]
        print(f"✓ Low risk transaction investigation: {data['risk_level']}")
    
    def test_investigate_with_related_memories(self):
        """Test investigation includes related memories."""
        payload = {
            "transaction_id": "txn_test_003",
            "customer": "Test Customer",
            "amount": 500.0,
            "currency": "USD",
            "location": "Test City",
            "merchant": "Test Merchant",
            "risk_score": 75,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert "related_memories" in data
        assert data["related_memories"] >= 0
        print(f"✓ Investigation found {data['related_memories']} related memories")
    
    def test_investigate_fraud_type_classification(self):
        """Test fraud type is properly classified."""
        payload = {
            "transaction_id": "txn_fraud_test_001",
            "customer": "Test Customer",
            "amount": 5000.0,
            "currency": "USD",
            "location": "Foreign Country",
            "merchant": "Unknown Merchant",
            "risk_score": 85,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert data["fraud_type"] is not None
        print(f"✓ Fraud type classified as: {data['fraud_type']}")
    
    def test_investigate_reasoning_provided(self):
        """Test investigation provides reasoning for decision."""
        payload = {
            "transaction_id": "txn_reasoning_test_001",
            "customer": "Test Customer",
            "amount": 500.0,
            "currency": "USD",
            "location": "Test City",
            "merchant": "Test Merchant",
            "risk_score": 75,
        }
        
        response = client.post("/investigate", json=payload)
        data = response.json()
        
        assert len(data["reasoning"]) > 0
        assert len(data["reasoning"]) >= 10  # Should have substantive reasoning
        print(f"✓ Reasoning provided: {data['reasoning'][:80]}...")
    
    def test_investigate_missing_fields(self):
        """Test investigation with incomplete payload."""
        incomplete_payload = {
            "transaction_id": "txn_incomplete_001",
            "customer": "Test Customer",
            # Missing other required fields
        }
        
        response = client.post("/investigate", json=incomplete_payload)
        # Should either accept with defaults or return 422
        assert response.status_code in [200, 422]
        print(f"✓ API handles incomplete payload gracefully (status: {response.status_code})")


class TestMemoryEndpoints:
    """Test memory-related endpoints."""
    
    def test_search_memories_endpoint(self):
        """Test memory search endpoint."""
        payload = {
            "query": "fraud",
            "limit": 5,
        }
        
        response = client.post("/search-memories", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("items", []), list)
        print(f"✓ Memory search returned {len(data.get('items', []))} results")
    
    def test_store_memory_endpoint(self):
        """Test memory storage endpoint."""
        payload = {
            "investigation_id": "inv_001",
            "title": "Test Memory",
            "content": "This is a test memory entry.",
            "risk_level": "High",
            "fraud_type": "Card Fraud",
            "confidence": 0.85,
            "learning_impact": "+5% detection",
        }
        
        response = client.post("/store-memory", json=payload)
        assert response.status_code == 200
        print("✓ Memory storage endpoint working")
    
    def test_get_memories_endpoint(self):
        """Test get all memories endpoint."""
        response = client.get("/memories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("items", []), list)
        print(f"✓ Retrieved {len(data.get('items', []))} memories")


class TestIntegration:
    """Integration tests combining multiple endpoints."""
    
    def test_full_investigation_workflow(self):
        """Test complete workflow: Get transactions -> Investigate -> Get memories."""
        # Step 1: Get transactions
        transactions_response = client.get("/transactions")
        assert transactions_response.status_code == 200
        transactions = transactions_response.json()["items"]
        print(f"✓ Step 1: Retrieved {len(transactions)} transactions")
        
        # Step 2: Investigate first transaction
        if transactions:
            txn = transactions[0]
            investigate_payload = {
                "transaction_id": str(txn.get("id", "txn_001")),
                "customer": txn.get("customer", "Test"),
                "amount": txn.get("amount", 100.0),
                "currency": txn.get("currency", "USD"),
                "location": txn.get("location", "Test City"),
                "merchant": txn.get("merchant", "Test Merchant"),
                "risk_score": txn.get("riskScore", 50),
            }
            
            investigation_response = client.post("/investigate", json=investigate_payload)
            assert investigation_response.status_code == 200
            investigation = investigation_response.json()
            print(f"✓ Step 2: Investigation completed - Risk: {investigation.get('risk_level')}")
            
            # Step 3: Get memories
            memories_response = client.get("/memories")
            assert memories_response.status_code == 200
            memories = memories_response.json()["items"]
            print(f"✓ Step 3: Retrieved {len(memories)} related memories")
    
    def test_dashboard_reflects_data(self):
        """Test dashboard reflects transaction and investigation data."""
        # Get dashboard data
        dashboard_response = client.get("/dashboard")
        assert dashboard_response.status_code == 200
        dashboard = dashboard_response.json()
        
        # Get transaction data
        transactions_response = client.get("/transactions")
        transactions = transactions_response.json()
        
        # Verify dashboard has transaction count
        assert dashboard["summary"]["totalTransactions"] == len(transactions["items"])
        print(f"✓ Dashboard reflects {dashboard['summary']['totalTransactions']} transactions")
        
        # Verify KPIs are present
        assert len(dashboard["kpis"]) > 0
        print(f"✓ Dashboard shows {len(dashboard['kpis'])} KPIs")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
