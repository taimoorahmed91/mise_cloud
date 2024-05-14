import json
import argparse

def compare_json_files(file1, file2):
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

            if data1 == data2:
                print("The JSON files are identical.")
                print("\n\n")
            else:
                print("The JSON files are not identical. Differences:")
                find_differences(data1, data2)
    except FileNotFoundError:
        print("One or both files not found.")
        print("\n\n")

def find_differences(obj1, obj2, path=""):
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        for key in set(obj1.keys()) | set(obj2.keys()):
            new_path = f"{path}.{key}" if path else key
            if key in obj1 and key in obj2:
                find_differences(obj1[key], obj2[key], new_path)
            elif key in obj1:
                print(f"Key '{new_path}' exists only in the first JSON file")
            else:
                print(f"Key '{new_path}' exists only in the second JSON file")
    elif isinstance(obj1, list) and isinstance(obj2, list):
        if len(obj1) != len(obj2):
            print(f"The array at '{path}' has different lengths.")
        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            find_differences(item1, item2, f"{path}[{i}]")
    else:
        if obj1 != obj2:
            print("\n\n")
            print(f"Value at '{path}':")
            print("\n")
            print(f"  First JSON:  {obj1}")
            print(f"  Second JSON: {obj2}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two JSON files.")
    parser.add_argument("file1", help="Path to the first JSON file")
    parser.add_argument("file2", help="Path to the second JSON file")
    args = parser.parse_args()
    compare_json_files(args.file1, args.file2)

