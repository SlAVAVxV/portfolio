import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
import joblib
import os

WINDOW_SIZE = 50
FEATURE_COLS = ['vibration', 'current', 'temperature', 'pressure']
THRESHOLD = 0.01

class PredictiveMaintenanceSystem:
    def __init__(self):
        self.scaler = RobustScaler()
        self.autoencoder = None
        self.iso_forest = None

    def build_autoencoder(self):
        inputs = Input(shape=(WINDOW_SIZE, len(FEATURE_COLS)))
        x = LSTM(64, activation='relu', return_sequences=True)(inputs)
        encoded = LSTM(32, activation='relu', return_sequences=False)(x)
        x = RepeatVector(WINDOW_SIZE)(encoded)
        x = LSTM(32, activation='relu', return_sequences=True)(x)
        x = LSTM(64, activation='relu', return_sequences=True)(x)
        decoded = TimeDistributed(Dense(len(FEATURE_COLS)))(x)
        autoencoder = Model(inputs, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')
        return autoencoder

    def train(self, data_path='data/normal_operation.csv'):
        df = pd.read_csv(data_path)
        scaled_data = self.scaler.fit_transform(df[FEATURE_COLS])
        joblib.dump(self.scaler, 'models/scaler.pkl')
        X = []
        for i in range(len(scaled_data) - WINDOW_SIZE):
            X.append(scaled_data[i:i+WINDOW_SIZE])
        X = np.array(X)
        self.autoencoder = self.build_autoencoder()
        self.autoencoder.fit(X, X, epochs=50, batch_size=32, validation_split=0.2, verbose=1)
        self.autoencoder.save('models/autoencoder.h5')
        encoder = Model(inputs=self.autoencoder.input,
                        outputs=self.autoencoder.layers[2].output)
        features = encoder.predict(X)
        self.iso_forest = IsolationForest(contamination=0.01, random_state=42)
        self.iso_forest.fit(features)
        joblib.dump(self.iso_forest, 'models/iso_forest.pkl')
        print("✅ Модели обучены и сохранены в /models.")

    def predict(self, window):
        scaled = self.scaler.transform(window)
        rec = self.autoencoder.predict(np.array([scaled]), verbose=0)
        mse = np.mean(np.square(scaled - rec[0]))
        encoder = Model(inputs=self.autoencoder.input,
                        outputs=self.autoencoder.layers[2].output)
        feat = encoder.predict(np.array([scaled]), verbose=0)
        anomaly = self.iso_forest.predict(feat)[0] == -1
        return {
            'mse': float(mse),
            'anomaly': bool(anomaly),
            'threshold': THRESHOLD,
            'status': '⚠️ ANOMALY' if anomaly else '✅ Normal'
        }