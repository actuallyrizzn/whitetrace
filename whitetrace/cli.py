import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress

from .processing.loader import load_image
from .processing.threshold import apply_threshold
from .processing.builder import build_white_transparent
from .processing.vectorize import vectorize_to_svg

app = typer.Typer()
console = Console()

@app.command()
def main(
    input_file: Path = typer.Argument(..., help="Path to input image file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Path to output file"),
    format: str = typer.Option("png", "--format", "-f", help="Output format (png, webp, svg)"),
    threshold: int = typer.Option(200, "--threshold", "-t", help="Threshold value (0-255)"),
    invert: bool = typer.Option(False, "--invert", "-i", help="Invert threshold result"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Output debug information")
):
    """
    Convert an image to white-on-transparent format.
    """
    try:
        # Determine output path
        if output is None:
            output = input_file.parent / f"{input_file.stem}_white.{format}"
        
        # Load and process image
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing image...", total=4)
            
            # Load image
            image = load_image(input_file)
            progress.update(task, advance=1)
            
            # Apply threshold
            binary = apply_threshold(image, threshold, invert)
            progress.update(task, advance=1)
            
            if format.lower() == 'svg':
                # Vectorize to SVG
                svg_content = vectorize_to_svg(binary)
                with open(output, 'w') as f:
                    f.write(svg_content)
            else:
                # Create white-on-transparent image
                result = build_white_transparent(binary)
                result.save(output, format.upper())
            
            progress.update(task, advance=2)
        
        console.print(f"[green]Successfully processed image: {output}")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 