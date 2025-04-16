# WhiteTrace

Convert images to white-on-transparent format. This tool takes an input image and converts it to a white silhouette on a transparent background.

## Installation

```bash
pip install whitetrace
```

## Usage

Basic usage:
```bash
whitetrace input.jpg
```

This will create `input_white.png` in the same directory.

### Options

- `--output`, `-o`: Specify output file path
- `--format`, `-f`: Output format (png, webp, svg)
- `--threshold`, `-t`: Threshold value (0-255, default: 200)
- `--invert`, `-i`: Invert threshold result
- `--debug`, `-d`: Output debug information

### Examples

Convert to PNG with custom threshold:
```bash
whitetrace input.jpg --threshold 150
```

Convert to SVG:
```bash
whitetrace input.jpg --format svg
```

Specify output file:
```bash
whitetrace input.jpg --output output.png
```

## Supported Formats

### Input
- JPG/JPEG
- PNG
- WEBP
- SVG

### Output
- PNG (default)
- WEBP
- SVG

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT 