Excellent—here’s your **robust, implementation-ready CLI spec** for the image processing tool. This spec assumes a Python-based implementation using industry-standard libraries and is designed to be built and extended by an autonomous or semi-autonomous agent swarm.

---

# 📐 Image Processor CLI Spec: *White-on-Transparent Converter*

## 🔧 Tool Name:
`whitetrace`

---

## 🎯 Purpose

Convert a given image (JPG, PNG, SVG, WEBP) into a **white-on-transparent** output image in the selected format (PNG, WEBP, SVG). Output highlights the foreground in solid white, removing background elements and retaining alpha transparency.

---

## 📥 Supported Input Formats

- `.jpg` / `.jpeg`
- `.png`
- `.webp`
- `.svg`

If the image is SVG, it must be **converted to a raster** internally before thresholding (see rasterization step).

---

## 📤 Supported Output Formats

- `.png` (default)
- `.webp`
- `.svg` (vectorized from thresholded bitmap)

---

## 🚀 CLI Usage

```bash
whitetrace input_file [--output OUTPUT_FILE] [--format {png,webp,svg}] [--threshold VALUE] [--invert] [--debug]
```

### 📘 Arguments:

| Flag | Description |
|------|-------------|
| `input_file` | Path to input image file |
| `--output` | Path to output file (if not specified, defaults to `input_white.<ext>`) |
| `--format` | Output format: `png`, `webp`, or `svg` (default: inferred from output filename or `png`) |
| `--threshold` | Threshold value (0–255) for binarization (default: 200) |
| `--invert` | Invert thresholding result (use if subject is lighter than background) |
| `--debug` | Outputs intermediary files (e.g., thresholded bitmap, alpha mask) for inspection |

---

## 🛠️ Pipeline (Per File)

1. **Load image**
   - Use Pillow for raster formats
   - For SVG: use `cairosvg` to rasterize to PNG before processing

2. **Convert to Grayscale**
   - Discard color data

3. **Apply Threshold**
   - Default: any pixel below `threshold` is foreground (white)
   - If `--invert`, reverse logic

4. **Construct Output Image**
   - **Foreground** pixels: `#FFFFFF` + full opacity
   - **Background** pixels: `#000000` + alpha 0 (fully transparent)

5. **Export**
   - `PNG` or `WEBP`: Save RGBA image
   - `SVG`: Vectorize the thresholded bitmap (e.g., via `potrace`) and output single white path on transparent canvas

---

## 📚 Dependencies

Python libraries:
- `Pillow`
- `numpy`
- `cairosvg` (for SVG input rasterization)
- `opencv-python` (optional, for adaptive thresholding)
- `potrace` (via subprocess or bindings for SVG vector output)

Optional:
- `typer` for CLI definition
- `rich` or `loguru` for enhanced CLI UX/logging

---

## 📂 Folder Structure (suggested)

```
whitetrace/
├── cli.py              # Main CLI entrypoint
├── processing/
│   ├── __init__.py
│   ├── loader.py       # Input handling (JPG/PNG/SVG/WEBP)
│   ├── threshold.py    # Grayscale + threshold
│   ├── builder.py      # Assemble white-on-transparent image
│   ├── vectorize.py    # Bitmap → SVG vector conversion
├── utils/
│   ├── file_utils.py   # Path handling, extension detection
│   ├── debug.py        # Intermediate file saving
├── tests/
│   └── test_whitetrace.py
└── requirements.txt
```

---

## 🧪 Testing Criteria

- ✅ Correct thresholding for dark-on-light and light-on-dark inputs
- ✅ Full support for alpha transparency
- ✅ Accurate SVG vector output (single-path white fill on transparent canvas)
- ✅ CLI handles batch conversion (stretch goal)
- ✅ Accepts large resolution inputs without crash (streaming optional)
- ✅ `--debug` generates intermediary visual assets

---

## 🧠 Stretch Goals

- Drag-and-drop GUI (using `tkinter` or Electron)
- Multi-threaded batch processor
- Web-based version using Streamlit or Flask
- Watch folder + auto-process mode

---

Let me know if you want me to write `requirements.txt`, a `pyproject.toml`, or `cli.py` scaffolding. Otherwise, this spec is production-grade and swarm-ready.