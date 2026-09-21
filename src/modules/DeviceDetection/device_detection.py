"""Device detection module."""

import torch
from modules.console_colors import ULTRASINGER_HEAD, red_highlighted, blue_highlighted

def check_gpu_support() -> tuple[str, str]:
    """Check the worker device supported by PyTorch."""

    print(f"{ULTRASINGER_HEAD} Checking GPU support for {blue_highlighted('pytorch')}.")

    pytorch_gpu_supported = torch.cuda.is_available()
    if not pytorch_gpu_supported:
        print(
            f"{ULTRASINGER_HEAD} {blue_highlighted('pytorch')} - there are no {red_highlighted('cuda')} devices available -> Using {red_highlighted('cpu')}."
        )
    else:
        print(f"{ULTRASINGER_HEAD} {blue_highlighted('pytorch')} - using {red_highlighted('cuda')} gpu.")

    device = "cuda" if pytorch_gpu_supported else "cpu"
    return device, device
