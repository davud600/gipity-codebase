import pyperclip
import sys
import os

if len(sys.argv) > 2 and os.path.isdir(sys.argv[1]):
    dir = sys.argv[1]
    files_to_extend = sys.argv[2].split(",")
elif len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    dir = sys.argv[1]
    files_to_extend = []
else:
    dir = "/home/davud/wood-chipper-ai"
    files_to_extend = []

IGNORE_DIR = [".pyc", ".lock", ".git", ".venv", "node_modules", ".sample", ".exe", ".env", ".csv", ".txt", ".json", "__pycache__"]
ACCEPT_FILE_EXTENSION = [".py", ".lua", ".js", ".ts", "jsx", ".tsx", ".md"]

def should_include_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext in ACCEPT_FILE_EXTENSION

def should_include_dir(dirname: str) -> bool:
    return dirname not in IGNORE_DIR

def sorted_files_first(path: str):
    items = os.listdir(path)

    def sort_key(name):
        full_path = os.path.join(path, name)
        is_dir = os.path.isdir(full_path)
        return (is_dir, name.lower())

    return sorted(items, key=sort_key)

def expand_file_or_dir(file_or_dir_path, content="", depth=0):
    file_or_dir_name = file_or_dir_path.split("/")[-1]

    if os.path.isfile(file_or_dir_path):
        if should_include_file(file_or_dir_name):
            content += f"\n{' '*depth}file: {file_or_dir_name}"

            if file_or_dir_name in files_to_extend:
                try:
                    with open(file_or_dir_path, "r") as f:
                        content += f"\n{file_or_dir_path}:\n```\n{f.read()}```"
                except Exception:
                    print("couldn't open file")

            return content

    elif os.path.isdir(file_or_dir_path):
        if should_include_dir(file_or_dir_name):
            new_depth = depth + 1
            content += f"\n{' '*depth}dir: {file_or_dir_name}"

            for l_file_or_dir in sorted_files_first(file_or_dir_path):
                content = expand_file_or_dir(os.path.join(file_or_dir_path, l_file_or_dir), content, new_depth)

            return content

    return content


if __name__ == "__main__":
    content = expand_file_or_dir(dir)
    pyperclip.copy(content)
    print(content)
