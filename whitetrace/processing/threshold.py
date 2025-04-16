from PIL import Image
import numpy as np
import cv2

def apply_threshold(image: Image.Image, threshold: int = 200, invert: bool = False) -> Image.Image:
    """
    Convert image to grayscale and apply threshold to create white-on-transparent output.
    
    Args:
        image: Input PIL Image
        threshold: Threshold value (0-255)
        invert: Whether to invert the threshold result
        
    Returns:
        Thresholded PIL Image with white foreground on transparent background
    """
    # Convert PIL image to grayscale first
    if image.mode != 'L':
        image = image.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale if not already
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Apply bilateral filter for noise reduction while preserving edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Calculate local standard deviation to identify detail areas
    kernel = np.ones((5,5), np.float32) / 25
    local_mean = cv2.filter2D(denoised.astype(float), -1, kernel)
    local_sqr_mean = cv2.filter2D(np.square(denoised.astype(float)), -1, kernel)
    local_std = np.sqrt(local_sqr_mean - np.square(local_mean)).astype(np.uint8)
    
    # Adaptive threshold with different parameters for detail vs non-detail areas
    detail_mask = local_std > 20
    
    # Process detail areas with fine-grained adaptive threshold
    detail_thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        7,  # Smaller block size for details
        2
    )
    
    # Process non-detail areas with larger block size
    nondetail_thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,  # Larger block size for smooth areas
        5
    )
    
    # Combine results based on detail mask
    result = np.where(detail_mask, detail_thresh, nondetail_thresh)
    
    # Apply global threshold as a refinement
    _, global_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    if invert:
        global_mask = cv2.bitwise_not(global_mask)
    
    # Combine with global threshold using soft masking
    alpha = 0.7
    result = cv2.addWeighted(result, alpha, global_mask, 1-alpha, 0)
    _, result = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)
    
    # Final cleanup
    kernel = np.ones((2,2), np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    
    # Create RGBA image (white on transparent)
    rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
    if invert:
        # If inverted, black pixels become white, and white pixels become transparent
        rgba[result == 0] = [255, 255, 255, 255]  # White with full opacity
        rgba[result == 255] = [0, 0, 0, 0]  # Transparent
    else:
        # White pixels become white, black pixels become transparent
        rgba[result == 255] = [255, 255, 255, 255]  # White with full opacity
        rgba[result == 0] = [0, 0, 0, 0]  # Transparent
    
    return Image.fromarray(rgba, 'RGBA') 