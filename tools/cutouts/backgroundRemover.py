import os
from pathlib import Path
from rembg import remove
from PIL import Image
import glob

# List of common image extensions to process
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

def create_cutouts_folder(script_dir):
    # Create cutouts folder in the same directory as the script
    cutouts_dir = script_dir / "cutouts"
    cutouts_dir.mkdir(exist_ok=True)
    return cutouts_dir

def remove_background(input_path, output_path):
    try:
        input_image = Image.open(input_path)
        
        # Convert to RGBA if the image doesn't have an alpha channel
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
            
        output_image = remove(input_image)
        # Always save as PNG to preserve transparency
        output_path = output_path.with_suffix('.png')
        output_image.save(output_path, format='PNG')
        print(f"Processed: {input_path.name}")
    except Exception as e:
        print(f"Error processing {input_path.name}: {str(e)}")

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Create cutouts folder
    cutouts_dir = create_cutouts_folder(script_dir)
    
    # Get all image files in the script's directory
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(list(script_dir.glob(f"*{ext}")))
        # Also check for uppercase extensions
        image_files.extend(list(script_dir.glob(f"*{ext.upper()}")))
    
    if not image_files:
        print(f"No image files found in: {script_dir}")
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return
    
    print(f"Found {len(image_files)} image files. Starting background removal...")
    
    # Process each image file
    for img_path in image_files:
        output_path = cutouts_dir / f"cutout_{img_path.stem}"
        remove_background(img_path, output_path)
    
    print("\nProcessing complete! Check the 'cutouts' folder for results.")

if __name__ == "__main__":
    main()