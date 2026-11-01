# 🚀 GPU Inference Optimization for Industrial CV

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![NVIDIA CUDA](https://img.shields.io/badge/NVIDIA-CUDA-76B900?style=for-the-badge&logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)

**Разработка для ООО «Связь Автоматика» (г. Томск)**  
*Ускорение нейросетевых моделей (ResNet-50) для систем промышленного компьютерного зрения (контроль СИЗ, детекция дефектов).*

## 📌 О проекте
Данный проект демонстрирует методы оптимизации инференса глубокого обучения на графических процессорах NVIDIA. 
**Проблема:** Базовая модель в формате FP32 работает слишком медленно (>14 мс на кадр) и потребляет много видеопамяти (~1.1 ГБ).
**Решение:** Применение смешанной точности (FP16), JIT-компиляции графа и оптимизации формата памяти.

## ⚡ Ключевые методы оптимизации
*   **FP16 (Mixed Precision):** Задействование Tensor Cores, снижение потребления VRAM.
*   **`torch.compile` (PyTorch 2.x):** Устранение накладных расходов интерпретатора Python.
*   **`channels_last`:** Оптимизация доступа к кэшу GPU при свёртках.
*   **`cudnn.benchmark = True`:** Автотюнинг алгоритмов свёртки NVIDIA.

## 📊 Результаты бенчмарка (на NVIDIA T4)
| Метрика | Baseline (FP32) | Optimized (FP16 + compile) | Эффект |
| :--- | :--- | :--- | :--- |
| **Latency (batch=1)** | ~14.5 мс | ~7.2–8.0 мс | **Ускорение 1.8–2.0×** |
| **Throughput** | ~69 FPS | ~125–139 FPS | Стабильно выше 30 FPS |
| **Peak VRAM** | ~1120 МБ | ~610–650 МБ | **Снижение ~45%** |
| **Top-1 Accuracy** | 76.1% | 75.9–76.0% | Δ ≤ 0.2% (погрешность) |

## 🛠️ Структура проекта
```text
svyaz-avtomatika-gpu-optimization/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    ├── model.py       # Загрузка ResNet-50 с оптимизацией
    ├── baseline.py    # Базовый инференс (FP32)
    ├── optimized.py   # Оптимизированный инференс (FP16 + compile)
    └── benchmark.py   # Скрипт сравнения и замеров
```

## 🚀 Установка и запуск
1. Установите зависимости:
```bash
pip install -r requirements.txt
```
2. Запустите бенчмарк:
```bash
python src/benchmark.py --batch-size 1 --iterations 100
```

---
**Автор:** Вячеслав Саранчин (SIAVAVXV)  
**Специальность:** Прикладная информатика (ИИ и большие данные)  
📬 [Telegram](https://t.me/SIAVAVXV) | 📧 svyacheslaw21@gmail.com