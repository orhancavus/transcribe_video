import torch

print(
    f"Torch availablec Check {torch.backends.mps.is_available()}"
)  # Should return True
