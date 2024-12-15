import os
import json

def explore_directory(path):
    try:
        tree = {}
        entries = os.listdir(path)
        entries.sort()
        
        for entry in entries:
            if entry == '.git':
                continue
                
            full_path = os.path.join(path, entry)
            
            if os.path.isdir(full_path):
                tree[entry] = explore_directory(full_path)
            else:
                tree[entry] = "file"
                
        return tree
                
    except PermissionError:
        return "Access denied"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    start_path = r"C:\Users\jhriv\OneDrive\Desktop\kleexck"
    tree = {os.path.basename(start_path): explore_directory(start_path)}
    
    # Save to tree.json in current directory
    with open('tree.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, indent=4)
    
    print("Directory structure saved to tree.json")

if __name__ == "__main__":
    main()