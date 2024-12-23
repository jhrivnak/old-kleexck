import os
from pathlib import Path
from rembg import remove
from PIL import Image
import glob

# List of common image extensions to process
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

def remove_background(input_path):
    try:
        input_image = Image.open(input_path)
        
        # Convert to RGBA if the image doesn't have an alpha channel
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
            
        output_image = remove(input_image)
        # Save the output file with the same name but with a .png extension
        output_path = input_path.with_suffix('.png')
        output_image.save(output_path, format='PNG')
        print(f"Processed: {input_path.name}")
        
        # Delete the original file after processing
        os.remove(input_path)
    except Exception as e:
        print(f"Error processing {input_path.name}: {str(e)}")

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    
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
        remove_background(img_path)
    
    print("\nProcessing complete! Files have been updated in the same folder.")

if __name__ == "__main__":
    main()
