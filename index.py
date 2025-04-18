import argparse
import os
import pyperclip

IGNORE_DIR = [".pyc", ".lock", ".git", ".venv", "node_modules", ".sample", ".exe", ".env", ".csv", ".txt", ".json", "__pycache__", "venv"]
DEFAULT_ACCEPT_FILE_EXTENSIONS = [".py", ".lua", ".js", ".ts", "jsx", ".tsx", ".md"]

EXPAND_FILES = []
ACCEPT_FILE_EXTENSIONS = DEFAULT_ACCEPT_FILE_EXTENSIONS


def should_expand_file(filename: str) -> bool:
    return filename in EXPAND_FILES if EXPAND_FILES else True

def should_include_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext in ACCEPT_FILE_EXTENSIONS

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
    file_or_dir_name = os.path.basename(file_or_dir_path)

    if os.path.isfile(file_or_dir_path):
        if should_include_file(file_or_dir_name):
            content += f"\n{' ' * depth}file: {file_or_dir_name}"

            if should_expand_file(file_or_dir_name):
                try:
                    with open(file_or_dir_path, "r") as f:
                        content += f"\n{file_or_dir_path}:\n```\n{f.read()}```"
                except Exception:
                    print(f"Couldn't open file: {file_or_dir_path}")

    elif os.path.isdir(file_or_dir_path):
        if should_include_dir(file_or_dir_name):
            new_depth = depth + 1
            content += f"\n{' ' * depth}dir: {file_or_dir_name}"

            for l_file_or_dir in sorted_files_first(file_or_dir_path):
                content = expand_file_or_dir(os.path.join(file_or_dir_path, l_file_or_dir), content, new_depth)

    return content


def parse_args():
    parser = argparse.ArgumentParser(description="Gipity: strip a codebase into a prompt-friendly format")
    parser.add_argument("directory", nargs="?", default="/home/davud/wood-chipper-ai", help="Directory to process")
    parser.add_argument("--expand", "-e", help="Comma-separated list of files to inline", default="")
    parser.add_argument("--extensions", "-x", help="Comma-separated list of accepted extensions", default=",".join(DEFAULT_ACCEPT_FILE_EXTENSIONS))
    parser.add_argument("--no-clipboard", action="store_true", help="Print only, don't copy to clipboard")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    content = expand_file_or_dir(args.directory)

    print(content)

    if not args.no_clipboard:
        pyperclip.copy(content)
        print("(copied to clipboard)")
