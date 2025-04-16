import numpy as np
import cv2
from PIL import Image
from typing import Dict, Tuple, Union

def calculate_edge_preservation(original: np.ndarray, processed: np.ndarray) -> float:
    """Calculate how well edges are preserved between original and processed images."""
    # Convert to grayscale if needed
    if len(original.shape) == 3:
        original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    
    # Detect edges in both images
    orig_edges = cv2.Canny(original, 50, 150)
    proc_edges = cv2.Canny(processed, 50, 150)
    
    # Calculate intersection over union of edges
    intersection = np.logical_and(orig_edges, proc_edges)
    union = np.logical_or(orig_edges, proc_edges)
    
    if np.sum(union) == 0:
        return 0.0
    
    return np.sum(intersection) / np.sum(union)

def calculate_content_preservation(original: np.ndarray, processed: np.ndarray) -> float:
    """Calculate how much of the original content is preserved."""
    if len(original.shape) == 3:
        original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    
    # Threshold both images to binary
    _, orig_binary = cv2.threshold(original, 127, 255, cv2.THRESH_BINARY)
    
    # Calculate the ratio of white pixels
    orig_content = np.sum(orig_binary > 0)
    proc_content = np.sum(processed > 0)
    
    if orig_content == 0:
        return 0.0
    
    return min(proc_content / orig_content, 1.0)

def calculate_noise_level(processed: np.ndarray) -> float:
    """Calculate the level of noise in the processed image."""
    kernel = np.ones((3,3), np.uint8)
    cleaned = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
    noise_pixels = np.sum(processed != cleaned)
    return 1.0 - (noise_pixels / processed.size)

def calculate_component_preservation(original: np.ndarray, processed: np.ndarray) -> float:
    """Calculate how well major components are preserved."""
    if len(original.shape) == 3:
        original = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    
    # Threshold original image
    _, orig_binary = cv2.threshold(original, 127, 255, cv2.THRESH_BINARY)
    
    # Get connected components
    orig_num_labels, _ = cv2.connectedComponents(orig_binary)
    proc_num_labels, _ = cv2.connectedComponents(processed)
    
    # Calculate ratio, penalize both too many and too few components
    ratio = proc_num_labels / orig_num_labels
    return max(0, 1.0 - abs(1.0 - ratio))

def evaluate_result(original: Union[Image.Image, np.ndarray], 
                   processed: Union[Image.Image, np.ndarray]) -> Dict[str, float]:
    """
    Evaluate the quality of image processing result.
    
    Args:
        original: Original image
        processed: Processed image
        
    Returns:
        Dictionary of quality metrics
    """
    # Convert PIL images to numpy arrays if needed
    if isinstance(original, Image.Image):
        original = np.array(original)
    if isinstance(processed, Image.Image):
        processed = np.array(processed)
    
    # Calculate all metrics
    edge_score = calculate_edge_preservation(original, processed)
    content_score = calculate_content_preservation(original, processed)
    noise_score = calculate_noise_level(processed)
    component_score = calculate_component_preservation(original, processed)
    
    # Calculate weighted average
    metrics = {
        'edge_preservation': edge_score,
        'content_preservation': content_score,
        'noise_quality': noise_score,
        'component_preservation': component_score
    }
    
    # Calculate overall score with weights
    weights = {
        'edge_preservation': 0.35,
        'content_preservation': 0.30,
        'noise_quality': 0.15,
        'component_preservation': 0.20
    }
    
    overall_score = sum(score * weights[metric] for metric, score in metrics.items())
    metrics['overall_score'] = overall_score
    
    return metrics

def find_optimal_parameters(image: Image.Image, 
                          process_func,
                          threshold_range: Tuple[int, int, int] = (150, 251, 10)
                          ) -> Tuple[Dict[str, Union[int, bool]], Dict[str, float]]:
    """
    Find optimal processing parameters for the given image.
    
    Args:
        image: Input image
        process_func: Function that takes (image, threshold, invert) and returns processed image
        threshold_range: Tuple of (start, end, step) for threshold values
        
    Returns:
        Tuple of (best parameters, best metrics)
    """
    best_score = -float('inf')
    best_params = None
    best_metrics = None
    
    for threshold in range(*threshold_range):
        for invert in [False, True]:
            # Process image with current parameters
            processed = process_func(image, threshold, invert)
            
            # Evaluate result
            metrics = evaluate_result(image, processed)
            score = metrics['overall_score']
            
            if score > best_score:
                best_score = score
                best_params = {'threshold': threshold, 'invert': invert}
                best_metrics = metrics
    
    return best_params, best_metrics 