import pandas as pd
from catboost import CatBoostClassifier
import joblib
import numpy as np
import os

class EquipmentRecommender:
    FEATURE_NAMES = [
        'environment', 'accuracy_class', 'pipe_diameter',
        'material', 'medium_temp', 'pressure', 'ex_zone'
    ]

    def __init__(self, model_path='models/catboost_model.cbm'):
        if os.path.exists(model_path):
            self.model = CatBoostClassifier()
            self.model.load_model(model_path)
        else:
            self.model = None
            print("⚠️  Модель не найдена. Используется демо-режим.")

    def train(self, data_path='data/specs.csv'):
        from sklearn.model_selection import train_test_split
        df = pd.read_csv(data_path)
        X = df[self.FEATURE_NAMES]
        y = df['device_model']
        cat_features = ['environment', 'material', 'ex_zone']
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = CatBoostClassifier(iterations=150, depth=6, random_seed=42, verbose=0)
        self.model.fit(X_tr, y_tr, cat_features=cat_features, eval_set=(X_te, y_te))
        self.model.save_model('models/catboost_model.cbm')
        print(f"✅ Модель обучена. Accuracy: {self.model.score(X_te, y_te):.2%}")

    def recommend(self, input_data: dict, top_n=3):
        if self.model is None:
            return {"recommendations": [], "status": "model not loaded"}
        df = pd.DataFrame([input_data])
        df = df.reindex(columns=self.FEATURE_NAMES, fill_value='unknown')
        probas = self.model.predict_proba(df)[0]
        classes = self.model.classes_
        top_idx = np.argsort(probas)[::-1][:top_n]
        return {
            "input": input_data,
            "recommendations": [
                {"model": str(classes[i]), "confidence": round(float(probas[i] * 100), 1)}
                for i in top_idx
            ]
        }