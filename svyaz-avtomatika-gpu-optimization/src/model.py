import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

def load_model(device: torch.device, optimize: bool = False) -> nn.Module:
    """Загружает ResNet-50. При optimize=True применяет FP16 и channels_last."""
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2).eval()
    if optimize:
        model = model.to(memory_format=torch.channels_last).half()
    return model.to(device)

def get_dummy_input(batch_size: int, device: torch.device, optimize: bool = False) -> torch.Tensor:
    """Генерирует тестовый входной тензор (имитация видеокадра)."""
    dtype = torch.float16 if optimize else torch.float32
    x = torch.randn(batch_size, 3, 224, 224, dtype=dtype, device=device)
    if optimize:
        x = x.to(memory_format=torch.channels_last)
    return x