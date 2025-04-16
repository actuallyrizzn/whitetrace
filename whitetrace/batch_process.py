import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from .processing.loader import load_image
from .processing.threshold import apply_threshold
from .processing.evaluator import find_optimal_parameters

app = typer.Typer()
console = Console()

def process_file(input_path: Path, output_dir: Path, progress: Progress, task: TaskID) -> tuple[bool, str]:
    """
    Process a single file and save the result to the output directory.
    """
    try:
        # Skip SVG files for now
        if input_path.suffix.lower() == '.svg':
            return False, "SVG files are not supported in this version"
            
        # Load image
        image = load_image(input_path)
        progress.update(task, advance=0.2)
        
        # Find optimal parameters
        best_params, metrics = find_optimal_parameters(
            image,
            apply_threshold,
            threshold_range=(150, 251, 10)
        )
        progress.update(task, advance=0.4)
        
        # Process with optimal parameters
        result = apply_threshold(image, best_params['threshold'], best_params['invert'])
        progress.update(task, advance=0.2)
        
        # Create output path
        output_path = output_dir / f"{input_path.stem}_white.png"
        
        # Save result
        result.save(output_path, 'PNG')
        progress.update(task, advance=0.2)
        
        return True, (str(output_path), best_params, metrics)
    except Exception as e:
        return False, str(e)

@app.command()
def batch_process(
    input_dir: Path = typer.Argument(..., help="Directory containing input images"),
    output_dir: Path = typer.Argument(..., help="Directory to save processed images"),
    show_metrics: bool = typer.Option(False, "--metrics", "-m", help="Show detailed metrics for each image")
):
    """
    Process all images in the input directory and save results to output directory.
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all image files (excluding SVG)
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        image_files.extend(input_dir.glob(f'*{ext}'))
        image_files.extend(input_dir.glob(f'*{ext.upper()}'))
    
    if not image_files:
        console.print("[yellow]No image files found in input directory!")
        raise typer.Exit(1)
    
    # Process files with progress bar
    results = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing images...", total=len(image_files))
        
        for input_file in image_files:
            file_task = progress.add_task(f"Processing {input_file.name}...", total=1.0)
            success, result = process_file(input_file, output_dir, progress, file_task)
            
            if success:
                output_path, params, metrics = result
                results.append({
                    'file': input_file.name,
                    'output': output_path,
                    'params': params,
                    'metrics': metrics
                })
                progress.print(f"[green]Processed: {input_file.name} -> {output_path}")
                progress.print(f"[blue]Parameters: threshold={params['threshold']}, invert={params['invert']}")
            else:
                progress.print(f"[red]Failed to process {input_file.name}: {result}")
            
            progress.update(task, advance=1)
            progress.remove_task(file_task)
    
    # Show summary
    console.print(f"\n[green]Successfully processed {len(results)} of {len(image_files)} files")
    console.print(f"Output directory: {output_dir}")
    
    # Show metrics table if requested
    if show_metrics and results:
        table = Table(title="Processing Metrics")
        table.add_column("File")
        table.add_column("Edge Preservation")
        table.add_column("Content Preservation")
        table.add_column("Noise Quality")
        table.add_column("Component Preservation")
        table.add_column("Overall Score")
        
        for result in results:
            metrics = result['metrics']
            table.add_row(
                result['file'],
                f"{metrics['edge_preservation']:.2f}",
                f"{metrics['content_preservation']:.2f}",
                f"{metrics['noise_quality']:.2f}",
                f"{metrics['component_preservation']:.2f}",
                f"{metrics['overall_score']:.2f}"
            )
        
        console.print(table)

if __name__ == "__main__":
    app() 