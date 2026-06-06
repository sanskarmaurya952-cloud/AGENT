"""
XGBoost Fraud Detection Model Training Script
Trains on credit card fraud dataset and saves the model
"""

import xgboost as xgb
import numpy as np
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "fraud_detection_xgboost.model"


def create_synthetic_fraud_dataset(n_samples: int = 1000) -> tuple:
    """
    Create synthetic credit card fraud dataset for training.
    Mimics the structure of public fraud datasets like Kaggle's Credit Card Fraud Dataset.
    """
    np.random.seed(42)
    
    # Generate features
    data = {
        "amount": np.random.exponential(100, n_samples),  # Transaction amounts
        "merchant_category": np.random.randint(0, 10, n_samples),  # Merchant categories
        "transaction_type": np.random.randint(0, 6, n_samples),  # Transaction types
        "time_of_day": np.random.randint(0, 24, n_samples),  # Hour of day
        "days_since_account_opened": np.random.exponential(200, n_samples),  # Account age
        "transaction_count_today": np.random.poisson(3, n_samples),  # Daily transaction count
        "location_mismatch": np.random.binomial(1, 0.1, n_samples),  # Location mismatch
        "velocity_score": np.random.uniform(0, 100, n_samples),  # Transaction velocity
    }
    
    df = pd.DataFrame(data)
    
    # Generate fraud labels based on risk factors
    fraud_probability = np.zeros(n_samples)
    
    # High-risk factors increase fraud probability
    fraud_probability[df["amount"] > 500] += 0.2
    fraud_probability[df["time_of_day"] < 6] += 0.1
    fraud_probability[df["location_mismatch"] == 1] += 0.4
    fraud_probability[df["velocity_score"] > 80] += 0.2
    fraud_probability[df["transaction_count_today"] > 10] += 0.15
    fraud_probability[df["days_since_account_opened"] < 30] += 0.1
    
    # Cap at 1.0 and convert to binary labels
    fraud_probability = np.minimum(fraud_probability, 1.0)
    labels = (np.random.random(n_samples) < fraud_probability).astype(int)
    
    # Add some noise: flip 5% of labels randomly
    noise_indices = np.random.choice(n_samples, size=int(0.05 * n_samples), replace=False)
    labels[noise_indices] = 1 - labels[noise_indices]
    
    logger.info(f"Dataset created: {n_samples} samples, {labels.sum()} fraud cases ({labels.sum()/n_samples*100:.1f}%)")
    
    X = df.values
    y = labels
    
    # Split into train/test (80/20)
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, X_test, y_test) -> xgb.Booster:
    """Train XGBoost model on fraud detection task."""
    logger.info("Preparing training data...")
    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    
    # XGBoost parameters optimized for fraud detection
    params = {
        "objective": "binary:logistic",  # Binary classification
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 1,
        "gamma": 0,
        "random_state": 42,
    }
    
    logger.info("Training XGBoost model...")
    
    evals = [(dtrain, "train"), (dtest, "test")]
    evals_result = {}
    
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=50,
        evals=evals,
        evals_result=evals_result,
        early_stopping_rounds=10,
        verbose_eval=5
    )
    
    logger.info(f"Training complete. Best score: {evals_result['test']['logloss'][-1]:.4f}")
    
    return model


def evaluate_model(model: xgb.Booster, X_test, y_test) -> dict:
    """Evaluate model performance on test set."""
    dtest = xgb.DMatrix(X_test, label=y_test)
    predictions = model.predict(dtest)
    
    # Convert probabilities to binary predictions (threshold=0.5)
    pred_labels = (predictions > 0.5).astype(int)
    
    # Calculate metrics
    true_positives = ((pred_labels == 1) & (y_test == 1)).sum()
    false_positives = ((pred_labels == 1) & (y_test == 0)).sum()
    true_negatives = ((pred_labels == 0) & (y_test == 0)).sum()
    false_negatives = ((pred_labels == 0) & (y_test == 1)).sum()
    
    accuracy = (true_positives + true_negatives) / len(y_test)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positives": int(true_positives),
        "false_positives": int(false_positives),
        "true_negatives": int(true_negatives),
        "false_negatives": int(false_negatives),
    }
    
    logger.info(f"Model Performance:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall:    {metrics['recall']:.4f}")
    logger.info(f"  F1 Score:  {metrics['f1_score']:.4f}")
    
    return metrics


def save_model(model: xgb.Booster, path: Path):
    """Save trained model to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(str(path))
    logger.info(f"Model saved to {path}")


def main():
    """Main training pipeline."""
    logger.info("Starting XGBoost fraud detection model training...")
    logger.info("=" * 60)
    
    # Create synthetic dataset
    logger.info("\n1. Creating synthetic fraud dataset...")
    X_train, X_test, y_train, y_test = create_synthetic_fraud_dataset(n_samples=10000)
    
    logger.info(f"   Training set: {X_train.shape[0]} samples")
    logger.info(f"   Test set: {X_test.shape[0]} samples")
    logger.info(f"   Features: {X_train.shape[1]}")
    
    # Train model
    logger.info("\n2. Training XGBoost model...")
    model = train_model(X_train, y_train, X_test, y_test)
    
    # Evaluate model
    logger.info("\n3. Evaluating model performance...")
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model
    logger.info("\n4. Saving model...")
    save_model(model, MODEL_PATH)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Training complete!")
    logger.info(f"Model saved: {MODEL_PATH}")
    logger.info(f"Model performance - F1 Score: {metrics['f1_score']:.4f}")


if __name__ == "__main__":
    main()
