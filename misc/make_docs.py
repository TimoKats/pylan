import ast
import os

introduction = """

Pylan is a Python library that simulates the impact of scheduled events over time. You can install the Python library using PyPi with the following command:

```
pip install pylan-lib
```

This code snippet shows some basic functionality when doing simulations.

```python
import matplotlib.pyplot as plt
from pylan import AddGrow, Item, Subtract

savings = Item(start_value=100)
dividends = AddGrow("90d", 100, "1y", 1.1) # the dividend will grow with 10% each year
growing_salary = AddGrow("1m", 2500, "1y", 1.2, offset_start="24d") # every month 24th
mortgage = Subtract("0 0 2 * *", 1500)  # cron support

savings.add_patterns([growing_salary, dividends, mortgage])
result = savings.run("2024-1-1", "2028-1-1")

x, y = result.plot_axes()

plt.plot(x, y)
plt.show()
```

There are 2 important classes in this library: Item and Pattern. A pattern is an abstract base class, with multiple implementations. These implementations resemble a time based pattern (e.g. add 10 every month, yearly inflation, etc). The Item is something that patterns can be added to, like a savings account.

"""

footer = """

## Schedule
---

Passed to patterns as a parameter. Accepts multiple formats.

#### Cron schedules
For example, "0 0 2 * *" runs on the second day of each month.

#### Timedelta strings
Combination of a count and timedelta. For example, 2d (every 2 days) 3m (every 3 months). Currently supports: years (y), months (m), weeks (w), days (d).

#### Timedelta lists
Same as timedelta, but then alternates between the schedules. For example, ["2d", "5d"] will be triggered after 2 days, then after 5 days, then after 2 days, etc...

#### Datetime lists
A list of datetime objects or str that resemble datetime objects. For example, ["2024-1-1", "2025-1-1"].

> **_NOTE:_**  The date format in pylan is yyyy-mm-dd. Currently this is not configurable.

"""


def extract_docstring(node):
    """Extract docstring from a node, if available."""
    docstring = ast.get_docstring(node).strip() if ast.get_docstring(node) else ""
    return docstring.replace("@public", "")


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
                if "@private" in class_docstring:
                    break
                if class_docstring:
                    f.write(f"\n---\n## Class: {node.name}\n\n")
                    f.write(f"{class_docstring}\n\n")

                # Iterate over methods in the class
                for method_node in node.body:
                    if isinstance(method_node, ast.FunctionDef):
                        method_docstring = extract_docstring(method_node)
                        method_docstring = convert_code_lines_to_block(method_docstring)
                        method_params = find_line(file_path, "def " + method_node.name)

                        if method_docstring and "@private" not in method_docstring:
                            f.write(f"#### {node.name}.{method_params}\n\n")
                            f.write(f"{method_docstring}\n\n")


def generate_docs_for_folder(folder_path, output_file):
    with open(output_file, "w") as f:
        f.write(introduction + "\n")
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                generate_markdown_doc_from_file(file_path, output_file)
    with open(output_file, "a") as f:
        f.write(footer + "\n")


# Example usage
if __name__ == "__main__":
    folder_path = "../pylan/"
    output_file = "docs.md"
    generate_docs_for_folder(folder_path, output_file)
