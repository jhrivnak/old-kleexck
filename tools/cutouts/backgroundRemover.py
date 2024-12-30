import os
from pathlib import Path
from PIL import Image

SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

def remove_white_background(input_path):
    try:
        input_image = Image.open(input_path)
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
        
        data = input_image.getdata()
        new_data = []
        for item in data:
            # Replace pure white with transparency
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        input_image.putdata(new_data)
        output_path = input_path.parent / f"{input_path.stem}_cutout.png"
        input_image.save(output_path, format='PNG')
        
        if output_path.exists():
            print(f"Processed: {input_path.name} -> {output_path.name}")
            os.remove(input_path)
        else:
            print(f"Failed to create output for: {input_path.name}")
    except Exception as e:
        print(f"Error processing {input_path.name}: {str(e)}")

def main():
    script_dir = Path(__file__).parent.absolute()
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(list(script_dir.glob(f"*{ext}")))
        image_files.extend(list(script_dir.glob(f"*{ext.upper()}")))
    if not image_files:
        print(f"No image files found in: {script_dir}")
        return
    print(f"Found {len(image_files)} image files. Starting background removal...")
    for img_path in image_files:
        remove_white_background(img_path)
    print("\nProcessing complete! Files have been updated in the same folder.")

if __name__ == "__main__":
    main()
