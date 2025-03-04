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


def select_directory(root_path: Path) -> str:
    """Navigate directories interactively and return the selected directory path."""
    current_path = os.path.abspath(root_path)

    while True:
        # Get directories in the current path
        dirs = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
        dirs.sort()

        # Display current path and available directories
        print(f"\nCurrent Directory: {current_path}\n")
        for i, directory in enumerate(dirs):
            print(f"{i}: {directory}")

        print("\nOptions:")
        print("  - Enter a number to navigate into a directory.")
        print("  - Type 'b' to go back.")
        print("  - Type 'n' to create a new directory.")
        print("  - Press Enter to select this directory.")

        choice = input("\nChoice: ").strip()

        if choice == "":
            return current_path  # User confirms selection

        elif choice.lower() == "b":
            parent_path = os.path.dirname(current_path)
            if parent_path != current_path:  # Prevent going above root
                current_path = parent_path

        elif choice.lower() == "n":
            new_dir_name = input("Enter new directory name: ").strip()
            if new_dir_name:
                new_dir_path = os.path.join(current_path, new_dir_name)
                try:
                    os.makedirs(new_dir_path, exist_ok=True)
                    print(f"Directory '{new_dir_name}' created.")
                except Exception as e:
                    print(f"Error creating directory: {e}")

        elif choice.isdigit():
            index = int(choice)
            if 0 <= index < len(dirs):
                current_path = os.path.join(current_path, dirs[index])

        else:
            print("Invalid choice, please try again.")

def to_camel_case(name):
    """Convert an underscore_separated string to CamelCase."""
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
    parser.add_argument("source_dir", help="Source directory where files should be generated")
    parser.add_argument("--create-class", action="store_true", help="Generate a class in the header and source file")
    parser.add_argument("--create-template", action="store_true", help="Generate a template file")
    
    args = parser.parse_args()

    directory = Path(args.source_dir)
    directory = Path(select_directory(directory))  # Pass the source directory argument to the selection function
    filename = get_filename_from_directory(directory)
    create_header_and_source_files(filename, directory, create_class=args.create_class, create_template=args.create_template)

if __name__ == "__main__":
    main()
