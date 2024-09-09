import os
import argparse
from pathlib import Path

def print_directories(start_dir):
    """Print directories and return a list of paths."""
    dirs = []
    print("\nAvailable directories:")
    for i, (root, subdirs, _) in enumerate(os.walk(start_dir)):
        dirs.append(root)
        print(f"[{i}] {root}")
    return dirs

def select_directory(start_dir):
    """Prompt user to select a directory."""
    dirs = print_directories(start_dir)
    choice = input("Enter the directory number to create files (or 'new' to create a new parent folder): ")
    if choice.lower() == 'new':
        new_folder = input("Enter the new folder name: ")
        selected_dir = Path(start_dir) / new_folder
        selected_dir.mkdir(exist_ok=True)
    else:
        selected_dir = Path(dirs[int(choice)])
    return selected_dir

def to_camel_case(name):
    """Convert an underscore-separated string to CamelCase."""
    return ''.join(word.capitalize() for word in name.split('_'))

def create_header_and_source_files(filename, directory, create_class=False, create_template=False):
    """Generate C++ header, source, and optionally template files."""
    header_file = directory / f"{filename}.hpp"
    source_file = directory / f"{filename}.cpp"
    template_file = directory / f"{filename}.tpp" if create_template else None
    include_guard = f"{filename.upper()}_HPP"
    class_name = to_camel_case(filename)  # Convert to CamelCase

    # Write header file
    with open(header_file, 'w') as hf:
        hf.write(f"#ifndef {include_guard}\n#define {include_guard}\n\n")
        if create_class:
            hf.write(f"class {class_name} {{\npublic:\n    {class_name}();\n    ~{class_name}();\n}};\n\n")
        hf.write(f"#endif // {include_guard}\n")

    # Write source file
    with open(source_file, 'w') as sf:
        sf.write(f"#include \"{header_file.name}\"\n\n")
        if create_class:
            sf.write(f"{class_name}::{class_name}() {{}}\n")
            sf.write(f"{class_name}::~{class_name}() {{}}\n")

    # Write template file if requested
    if template_file:
        with open(template_file, 'w') as tf:
            tf.write(f"// Template implementation for {class_name}\n")

    print(f"Files '{header_file}', '{source_file}'" + (f", and '{template_file}'" if create_template else "") + " have been generated.")

def main():
    parser = argparse.ArgumentParser(description="C++ File Generator with Class and Template Support")
    parser.add_argument("source_dir", help="Source directory where files should be generated")
    parser.add_argument("--create-class", action="store_true", help="Generate a class in the header and source file")
    parser.add_argument("--create-template", action="store_true", help="Generate a template file")
    
    args = parser.parse_args()

    directory = Path(args.source_dir)
    filename = input("Enter the filename (without extension): ")
    directory = select_directory(directory)  # Pass the source directory argument to the selection function
    create_header_and_source_files(filename, directory, create_class=args.create_class, create_template=args.create_template)

if __name__ == "__main__":
    main()
