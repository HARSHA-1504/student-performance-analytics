"""
Student Performance Machine Learning Module

This module trains a Random Forest classifier to predict student pass/fail outcomes
based on academic and behavioral features.
"""

import os
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data"
MODEL_FILE = os.path.join(DATA_DIR, "passfail_model.pkl")
PROCESSED_FILE = os.path.join(DATA_DIR, "students_processed.csv")

# Feature selection based on domain knowledge and correlation analysis
FEATURES = ['studytime', 'failures', 'absences', 'G1', 'G2']


def load_data():
    """
    Load and prepare the processed dataset.
    
    Returns:
        tuple: (X, y) feature matrix and target vector
    """
    try:
        if not os.path.exists(PROCESSED_FILE):
            raise FileNotFoundError(f"Processed data file not found: {PROCESSED_FILE}")
        
        df = pd.read_csv(PROCESSED_FILE)
        logger.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
        
        # Convert pass/fail text to binary target
        df['target'] = df['final_result'].apply(lambda x: 1 if x == 'pass' else 0)
        
        # Check if all required features exist
        missing_features = [f for f in FEATURES if f not in df.columns]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        X = df[FEATURES]
        y = df['target']
        
        logger.info(f"Selected features: {FEATURES}")
        logger.info(f"Target distribution: {y.value_counts().to_dict()}")
        
        return X, y
        
    except Exception as e:
        logger.error(f"❌ Error loading data: {str(e)}")
        raise


def train_model(X, y):
    """
    Train the Random Forest classifier.
    
    Args:
        X: Feature matrix
        y: Target vector
        
    Returns:
        tuple: (model, X_test, y_test, y_pred) trained model and test results
    """
    try:
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set: {X_train.shape[0]} samples")
        logger.info(f"Test set: {X_test.shape[0]} samples")
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        model.fit(X_train, y_train)
        logger.info("✅ Model training completed")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        return model, X_test, y_test, y_pred
        
    except Exception as e:
        logger.error(f"❌ Error training model: {str(e)}")
        raise


def evaluate_model(y_test, y_pred):
    """
    Evaluate model performance and display results.
    
    Args:
        y_test: True labels
        y_pred: Predicted labels
    """
    try:
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model Accuracy: {accuracy:.4f}")
        
        print(f"\n{'='*50}")
        print("MODEL EVALUATION RESULTS")
        print(f"{'='*50}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print(f"\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        return accuracy
        
    except Exception as e:
        logger.error(f"❌ Error evaluating model: {str(e)}")
        raise


def save_model(model):
    """
    Save the trained model to disk.
    
    Args:
        model: Trained model to save
    """
    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Save model
        joblib.dump(model, MODEL_FILE)
        logger.info(f"✅ Model saved to {MODEL_FILE}")
        
    except Exception as e:
        logger.error(f"❌ Error saving model: {str(e)}")
        raise


def main():
    """
    Main machine learning pipeline execution.
    """
    try:
        logger.info("🚀 Starting ML pipeline...")
        
        # Load data
        X, y = load_data()
        
        # Train model
        model, X_test, y_test, y_pred = train_model(X, y)
        
        # Evaluate model
        accuracy = evaluate_model(y_test, y_pred)
        
        # Save model
        save_model(model)
        
        logger.info(f"🎯 ML pipeline completed successfully with {accuracy:.4f} accuracy")
        
    except Exception as e:
        logger.error(f"❌ ML pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
