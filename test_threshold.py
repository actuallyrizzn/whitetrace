import os
from PIL import Image
from whitetrace.processing.threshold import apply_threshold

def process_images():
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Test images with different parameters
    test_configs = [
        {'threshold': 200, 'invert': False},  # Default settings
        {'threshold': 200, 'invert': True},   # Inverted
        {'threshold': 150, 'invert': False},  # Lower threshold
    ]
    
    # Process each image in assets folder
    for filename in os.listdir('assets'):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join('assets', filename)
            
            try:
                # Open image
                with Image.open(input_path) as img:
                    # Process with each configuration
                    for i, config in enumerate(test_configs):
                        # Create output filename
                        base_name = os.path.splitext(filename)[0]
                        output_name = f"{base_name}_thresh{config['threshold']}"
                        if config['invert']:
                            output_name += "_inv"
                        output_name += ".png"
                        output_path = os.path.join('output', output_name)
                        
                        # Process and save
                        result = apply_threshold(img, **config)
                        result.save(output_path)
                        print(f"Processed {filename} with config {config}")
                        
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_images() 