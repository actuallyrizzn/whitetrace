from pathlib import Path
from typing import Union
from PIL import Image

def load_image(input_path: Union[str, Path]) -> Image.Image:
    """
    Load an image from the given path.
    
    Args:
        input_path: Path to the input image file
        
    Returns:
        PIL Image object
    """
    return Image.open(input_path) 