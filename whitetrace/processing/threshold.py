from PIL import Image
import numpy as np

def apply_threshold(image: Image.Image, threshold: int = 200, invert: bool = False) -> Image.Image:
    """
    Convert image to grayscale and apply threshold.
    
    Args:
        image: Input PIL Image
        threshold: Threshold value (0-255)
        invert: Whether to invert the threshold result
        
    Returns:
        Thresholded PIL Image
    """
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to numpy array for processing
    img_array = np.array(image)
    
    # Apply threshold
    if invert:
        mask = img_array > threshold
    else:
        mask = img_array < threshold
    
    # Create binary image
    binary = np.zeros_like(img_array)
    binary[mask] = 255
    
    return Image.fromarray(binary) 