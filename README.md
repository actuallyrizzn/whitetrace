# WhiteTrace

A powerful image processing tool that converts images to white-on-transparent format, optimized for logos and graphics.

## Features

- Converts various image formats (JPG, PNG, SVG, WEBP) to white-on-transparent PNG/WEBP/SVG
- Smart edge detection and detail preservation
- Adaptive thresholding for optimal results on different image types
- Handles both light-on-dark and dark-on-light inputs
- Maintains fine details while reducing noise
- Command-line interface for easy integration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Basic usage:
```bash
whitetrace input_file [--output OUTPUT_FILE] [--format {png,webp,svg}] [--threshold VALUE] [--invert] [--debug]
```

Arguments:
- `input_file`: Path to input image file
- `--output`: Path to output file (default: `input_white.<ext>`)
- `--format`: Output format: `png`, `webp`, or `svg` (default: inferred from output filename or `png`)
- `--threshold`: Threshold value 0-255 (default: 200)
- `--invert`: Invert thresholding result (use if subject is lighter than background)
- `--debug`: Output intermediary files for inspection

### Python API

```python
from whitetrace.processing.threshold import apply_threshold
from PIL import Image

# Load image
image = Image.open('input.png')

# Process image
result = apply_threshold(
    image,
    threshold=200,  # Adjust threshold (0-255)
    invert=False    # Set True for light-on-dark images
)

# Save result
result.save('output.png')
```

## Technical Details

### Processing Pipeline

1. **Image Loading**
   - Supports JPG, PNG, SVG, WEBP inputs
   - SVG files are rasterized before processing

2. **Preprocessing**
   - RGB to grayscale conversion
   - Bilateral filtering for noise reduction
   - Local standard deviation calculation for detail detection

3. **Adaptive Thresholding**
   - Detail-aware processing with dual thresholding
   - Fine-grained threshold for detailed areas
   - Larger block size for smooth regions

4. **Transparency Handling**
   - Converts binary mask to RGBA
   - White foreground (#FFFFFF) with full opacity
   - Transparent background (alpha = 0)

## Known Limitations

1. SVG output quality depends on vectorization accuracy
2. Very fine details might be lost in some cases
3. Complex gradients may not be preserved
4. Performance impact on very large images

## Planned Improvements

1. **Algorithm Enhancements**
   - Machine learning-based edge detection
   - Improved gradient handling
   - Better preservation of small text
   - Multi-scale processing for better detail retention

2. **Feature Additions**
   - Batch processing with parallel execution
   - GUI interface
   - Watch folder functionality
   - Preview mode
   - Custom color support
   - Additional output formats

3. **Performance Optimization**
   - GPU acceleration
   - Streaming processing for large files
   - Memory usage optimization
   - Caching mechanism for batch processing

4. **Quality Improvements**
   - Advanced noise reduction
   - Better handling of anti-aliased edges
   - Improved SVG vectorization
   - Support for preserving metadata

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC-BY-SA).

This means you are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose

Under the following terms:
- Attribution — You must give appropriate credit
- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

For more details: https://creativecommons.org/licenses/by-sa/4.0/

## Credits

Created and maintained by the WhiteTrace development team. 