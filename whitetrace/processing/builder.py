from PIL import Image
import numpy as np

def build_white_transparent(binary_image: Image.Image) -> Image.Image:
    """
    Convert binary image to white-on-transparent image.
    
    Args:
        binary_image: Binary PIL Image (0 and 255 values)
        
    Returns:
        RGBA PIL Image with white foreground and transparent background
    """
    # Convert to numpy array
    binary_array = np.array(binary_image)
    
    # Create RGBA array
    rgba = np.zeros((*binary_array.shape, 4), dtype=np.uint8)
    
    # Set white foreground (255, 255, 255, 255)
    mask = binary_array == 255
    rgba[mask] = [255, 255, 255, 255]
    
    # Set transparent background (0, 0, 0, 0)
    rgba[~mask] = [0, 0, 0, 0]
    
    return Image.fromarray(rgba, 'RGBA') 