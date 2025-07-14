import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
import joblib

BASE_DIR      = os.path.dirname(os.path.dirname(__file__))
DATASET_FILE  = os.path.join(BASE_DIR, 'ml_dataset.csv')
MODEL_DIR     = os.path.join(BASE_DIR, 'models')
MODEL_FILE    = os.path.join(MODEL_DIR, 'model.pkl')

def load_dataset(label_col="label_1d"):
    df = pd.read_csv(DATASET_FILE, index_col=0)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    X = df.drop(columns=['label_1d', 'label_2d', 'symbol', 'return_1d', 'return_2d'])
    y = df[label_col]
    return X, y

def train(label_col="label_1d"):
    X, y = load_dataset(label_col=label_col)
    param_grid = {
        "max_depth": [3, 4, 5],
        "n_estimators": [100, 150],
        "learning_rate": [0.1, 0.05],
    }
    model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=42)
    grid = GridSearchCV(model, param_grid, scoring='f1', cv=3, verbose=1, n_jobs=-1)
    grid.fit(X, y)
    best_model = grid.best_estimator_

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    print(f"Accuracy: {acc:.4f}  Precision: {prec:.4f}  Recall: {rec:.4f}  F1: {f1:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_FILE)
    print(f"✔️ Model kaydedildi → {MODEL_FILE}")

if __name__ == "__main__":
    train(label_col="label_1d")  
