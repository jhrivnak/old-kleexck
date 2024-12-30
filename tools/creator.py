import os

# Define the directory structure
structure = {
    "src": {
        "components": ["Game.tsx"],
        "types": ["game.ts"],
        "": ["App.tsx", "index.tsx"]
    },
    "public": ["index.html"],
    "": ["tsconfig.json", "package.json"]
}

# Base directory
base_dir = r"C:\Users\jhriv\OneDrive\Documents\kleexck"

# Function to create the directory structure
def create_structure(base_path, structure):
    for key, value in structure.items():
        if isinstance(value, dict):
            # Create a directory and recurse
            dir_path = os.path.join(base_path, key)
            os.makedirs(dir_path, exist_ok=True)
            create_structure(dir_path, value)
        elif isinstance(value, list):
            # Create files in the current directory
            for file_name in value:
                file_path = os.path.join(base_path, file_name)
                with open(file_path, 'w') as f:
                    pass

# Create the structure
create_structure(base_dir, structure)

print(f"Directory structure created at {base_dir}.")
