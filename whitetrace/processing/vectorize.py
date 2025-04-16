import subprocess
import tempfile
from pathlib import Path
from PIL import Image

def vectorize_to_svg(binary_image: Image.Image) -> str:
    """
    Convert binary image to SVG using potrace.
    
    Args:
        binary_image: Binary PIL Image
        
    Returns:
        SVG string
    """
    # Save binary image to temporary file
    with tempfile.NamedTemporaryFile(suffix='.pbm', delete=False) as tmp:
        binary_image.save(tmp.name, 'PPM')
        tmp_path = tmp.name
    
    # Run potrace to convert to SVG
    svg_path = str(Path(tmp_path).with_suffix('.svg'))
    subprocess.run(['potrace', tmp_path, '-s', '-o', svg_path])
    
    # Read SVG content
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    # Clean up temporary files
    Path(tmp_path).unlink()
    Path(svg_path).unlink()
    
    return svg_content 