import os
import json

def explore_directory(path, ignored_extensions=None, ignored_folders=None):
    if ignored_extensions is None:
        ignored_extensions = []
    if ignored_folders is None:
        ignored_folders = []

    try:
        tree = {}
        entries = os.listdir(path)
        entries.sort()

        for entry in entries:
            full_path = os.path.join(path, entry)

            # Skip ignored folders
            if os.path.isdir(full_path) and entry in ignored_folders:
                continue

            if os.path.isdir(full_path):
                tree[entry] = explore_directory(full_path, ignored_extensions, ignored_folders)
            else:
                # Skip ignored file extensions
                if any(entry.endswith(ext) for ext in ignored_extensions):
                    continue
                tree[entry] = "file"

        return tree

    except PermissionError:
        return "Access denied"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    ignored_extensions = ['.dll', '.tsx', '.tmx']  
    ignored_folders = ['__pycache__', 'tools', 'objects'] 

    start_path = r"C:\Users\jhriv\OneDrive\Desktop\kleexck"
    tree = {os.path.basename(start_path): explore_directory(start_path, ignored_extensions, ignored_folders)}

    # Save to tree.json in current directory
    with open('tree.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, indent=4)

    print("Directory structure saved to tree.json")

if __name__ == "__main__":
    main()
