import ast
import os


def extract_docstring(node):
    """Extract docstring from a node, if available."""
    return ast.get_docstring(node).strip() if ast.get_docstring(node) else ""


def convert_code_lines_to_block(markdown_string):
    """Convert lines starting with '>>>' to Markdown code blocks."""
    lines = markdown_string.split("\n")
    in_code_block = False
    result = []

    for line in lines:
        if line.strip().startswith(">>>") and not in_code_block:
            result.append("```python")
            in_code_block = True
        elif in_code_block and not line.strip().startswith(">>>"):
            result.append("```")
            in_code_block = False
        result.append(line)

    if in_code_block:
        result.append("```")

    return "\n".join(result)


def find_line(file_path, sample_text):
    with open(file_path, "r") as file:
        for line in file:
            if sample_text in line:
                return line.strip()[4:]
    return "Sample text not found in the file."


def generate_markdown_doc_from_file(file_path, output_file):
    with open(file_path, "r") as file:
        file_content = file.read()

    # Parse the file content into an AST
    tree = ast.parse(file_content)

    with open(output_file, "a") as f:
        # Extract module-level docstring
        module_docstring = extract_docstring(tree)
        if module_docstring:
            f.write(f"{module_docstring}\n\n")

        # Iterate over functions and classes
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                class_docstring = extract_docstring(node)
                class_docstring = convert_code_lines_to_block(class_docstring)
                if class_docstring:
                    f.write(f"## Class: {node.name}\n\n")
                    f.write(f"{class_docstring}\n\n")

                # Iterate over methods in the class
                for method_node in node.body:
                    if isinstance(method_node, ast.FunctionDef):
                        method_docstring = extract_docstring(method_node)
                        method_docstring = convert_code_lines_to_block(method_docstring)
                        method_params = find_line(file_path, "def " + method_node.name)

                        if method_docstring and "@private" not in method_docstring:
                            f.write(f"#### {method_params}\n\n")
                            f.write(f"{method_docstring}\n\n")

                f.write("---\n")


def generate_docs_for_folder(folder_path, output_file):
    with open(output_file, "w") as f:
        f.write("Pylan is a library for simulating numeric patterns over time series.\n")
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                generate_markdown_doc_from_file(file_path, output_file)


# Example usage
if __name__ == "__main__":
    folder_path = "../pylan/"
    output_file = "docs.md"
    generate_docs_for_folder(folder_path, output_file)
