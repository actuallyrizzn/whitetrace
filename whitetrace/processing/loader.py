from pathlib import Path
from typing import Union
from PIL import Image
import cairosvg
import io

def load_image(input_path: Union[str, Path]) -> Image.Image:
    """
    Load an image from the given path, handling different formats including SVG.
    
    Args:
        input_path: Path to the input image file
        
    Returns:
        PIL Image object
    """
    input_path = Path(input_path)
    
    if input_path.suffix.lower() in ['.svg']:
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(url=str(input_path))
        return Image.open(io.BytesIO(png_data))
    else:
        return Image.open(input_path) 