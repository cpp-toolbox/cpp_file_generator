import os
import argparse
from pathlib import Path

from user_input.main import *
from text_utils.main import *

# TODO: one day replace this with my cpp_utils python code.
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

def get_filename_from_directory(directory: Path) -> str:
    """
    Ask the user if they want to use the last part of the selected directory as the filename.
    If not, allow them to enter a filename manually.
    
    :param directory: The selected directory path.
    :return: The filename without an extension.
    """
    suggested_filename = directory.name  # Last part of the directory path
    user_input = input(f"Use '{suggested_filename}' as the filename? (y/n): ").strip().lower()

    if user_input == 'y':
        return suggested_filename
    else:
        while True:
            custom_filename = input("Enter the desired filename (without extension): ").strip()
            if custom_filename:
                return custom_filename
            print("Filename cannot be empty. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="C++ File Generator with Class and Template Support")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search-dir", action="store_true", help="Interactively search for a directory to generate files in")
    group.add_argument("--dir", type=str, help="Directly specify the directory to generate files in")

    parser.add_argument("--create-class", action="store_true", help="Generate a class in the header and source file")
    parser.add_argument("--create-template", action="store_true", help="Generate a template file")

    args = parser.parse_args()

    if args.search_dir:
        directory = Path(interactively_select_directory(Path.cwd()))
    else:
        directory = Path(args.dir)
        directory.mkdir(parents=True, exist_ok=True)

    filename = get_filename_from_directory(directory)
    create_header_and_source_files(
        filename,
        directory,
        create_class=args.create_class,
        create_template=args.create_template
    )

if __name__ == "__main__":
    main()
