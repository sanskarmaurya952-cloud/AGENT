"""
XGBoost-based Fraud Detection Service
Uses credit card fraud patterns to detect suspicious transactions
"""

import xgboost as xgb
import numpy as np
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Model file path
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "fraud_detection_xgboost.model"


class FraudDetectionService:
    """XGBoost-based fraud detection model."""
    
    def __init__(self):
        """Initialize the fraud detection service."""
        self.model = None
        self.feature_names = [
            "amount",
            "merchant_category_encoded",
            "transaction_type_encoded",
            "time_of_day",
            "days_since_account_opened",
            "transaction_count_today",
            "location_mismatch",
            "velocity_score"
        ]
        self.merchant_categories = {
            "grocery": 0, "gas": 1, "dining": 2, "retail": 3, "travel": 4,
            "online": 5, "utilities": 6, "entertainment": 7, "healthcare": 8, "other": 9
        }
        self.transaction_types = {
            "online": 0, "atm": 1, "pos": 2, "phone": 3, "mail": 4, "recurring": 5
        }
        self._load_model()
    
    def _load_model(self):
        """Load or initialize the XGBoost model."""
        if MODEL_PATH.exists():
            try:
                self.model = xgb.Booster()
                self.model.load_model(str(MODEL_PATH))
                logger.info(f"Loaded XGBoost model from {MODEL_PATH}")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}. Using fallback scoring.")
                self.model = None
        else:
            logger.warning(f"Model file not found at {MODEL_PATH}. Using fallback scoring.")
            self.model = None
    
    def _encode_merchant_category(self, category: str) -> int:
        """Encode merchant category to integer."""
        category_lower = category.lower()
        return self.merchant_categories.get(category_lower, 9)  # Default to 'other'
    
    def _encode_transaction_type(self, txn_type: str) -> int:
        """Encode transaction type to integer."""
        txn_type_lower = txn_type.lower()
        return self.transaction_types.get(txn_type_lower, 5)  # Default to 'recurring'
    
    def _prepare_features(
        self,
        amount: float,
        merchant_category: str,
        transaction_type: str,
        time_of_day: int,
        days_since_account_opened: int,
        transaction_count_today: int,
        location_mismatch: bool,
        velocity_score: float
    ) -> np.ndarray:
        """Prepare features for model prediction."""
        features = np.array([
            amount,
            self._encode_merchant_category(merchant_category),
            self._encode_transaction_type(transaction_type),
            time_of_day,
            days_since_account_opened,
            transaction_count_today,
            int(location_mismatch),
            velocity_score
        ]).reshape(1, -1)
        
        return features
    
    def _fallback_scoring(
        self,
        amount: float,
        merchant_category: str,
        transaction_type: str,
        time_of_day: int,
        days_since_account_opened: int,
        transaction_count_today: int,
        location_mismatch: bool,
        velocity_score: float
    ) -> dict:
        """Fallback rule-based scoring when model not available."""
        risk_score = 0.0
        features_importance = {}
        
        # Amount scoring
        if amount > 10000:
            risk_score += 30
            features_importance["large_amount"] = 30
        elif amount > 5000:
            risk_score += 15
            features_importance["medium_amount"] = 15
        
        # Merchant category scoring
        high_risk_merchants = ["online", "travel", "entertainment"]
        if merchant_category.lower() in high_risk_merchants:
            risk_score += 15
            features_importance["merchant_category"] = 15
        
        # Transaction type scoring
        if transaction_type.lower() in ["online", "phone", "mail"]:
            risk_score += 15
            features_importance["transaction_type"] = 15
        
        # Time of day scoring (off-hours risky)
        if time_of_day < 6 or time_of_day > 23:
            risk_score += 15
            features_importance["off_hours"] = 15
        
        # New account scoring
        if days_since_account_opened < 30:
            risk_score += 20
            features_importance["new_account"] = 20
        elif days_since_account_opened < 90:
            risk_score += 10
            features_importance["young_account"] = 10
        
        # Transaction frequency scoring
        if transaction_count_today > 10:
            risk_score += 20
            features_importance["high_frequency"] = 20
        elif transaction_count_today > 5:
            risk_score += 10
            features_importance["medium_frequency"] = 10
        
        # Location mismatch scoring
        if location_mismatch:
            risk_score += 25
            features_importance["location_mismatch"] = 25
        
        # Velocity score impact
        if velocity_score > 80:
            risk_score += 25
            features_importance["high_velocity"] = 25
        elif velocity_score > 50:
            risk_score += 15
            features_importance["medium_velocity"] = 15
        
        # Cap at 100
        risk_score = min(risk_score, 100.0)
        
        # Determine confidence (lower for fallback)
        confidence = 65.0
        
        return {
            "risk_score": risk_score,
            "confidence": confidence,
            "features_importance": features_importance
        }
    
    def score(
        self,
        amount: float,
        merchant_category: str,
        transaction_type: str,
        time_of_day: int,
        days_since_account_opened: int,
        transaction_count_today: int,
        location_mismatch: bool,
        velocity_score: float
    ) -> dict:
        """Score a transaction for fraud risk."""
        features = self._prepare_features(
            amount,
            merchant_category,
            transaction_type,
            time_of_day,
            days_since_account_opened,
            transaction_count_today,
            location_mismatch,
            velocity_score
        )
        
        # Try model-based scoring if available
        if self.model:
            try:
                dmatrix = xgb.DMatrix(features)
                fraud_probability = self.model.predict(dmatrix)[0]
                risk_score = float(fraud_probability * 100)
                confidence = 85.0
                
                # Feature importance approximation
                features_importance = self._get_feature_importance(
                    amount, transaction_count_today, location_mismatch, velocity_score
                )
                
                return {
                    "risk_score": risk_score,
                    "confidence": confidence,
                    "features_importance": features_importance
                }
            except Exception as e:
                logger.warning(f"Model scoring failed: {str(e)}. Using fallback.")
        
        # Fallback rule-based scoring
        return self._fallback_scoring(
            amount,
            merchant_category,
            transaction_type,
            time_of_day,
            days_since_account_opened,
            transaction_count_today,
            location_mismatch,
            velocity_score
        )
    
    def _get_feature_importance(
        self,
        amount: float,
        transaction_count_today: int,
        location_mismatch: bool,
        velocity_score: float
    ) -> dict:
        """Get top feature importance contributions."""
        importance = {}
        
        if amount > 5000:
            importance["transaction_amount"] = 25
        if transaction_count_today > 5:
            importance["transaction_frequency"] = 20
        if location_mismatch:
            importance["location_mismatch"] = 30
        if velocity_score > 50:
            importance["velocity_score"] = 25
        
        return importance if importance else {"standard_transaction": 100}


# Global instance
_fraud_service = None


def get_fraud_service() -> FraudDetectionService:
    """Get or initialize the fraud detection service."""
    global _fraud_service
    if _fraud_service is None:
        _fraud_service = FraudDetectionService()
    return _fraud_service
