"""
Stkonstkoff package
"""

import os
import importlib

# Get the current directory (assuming __init__.py is in the top-level package directory)
package_directory = os.path.dirname(__file__)

# Traverse the directory structure
for root, dirs, files in os.walk(package_directory):
    # Exclude subdirectories with special names (e.g., "__pycache__")
    dirs[:] = [d for d in dirs if not d.startswith("__")]

    for file in files:
        # Exclude non-Python files
        if file.endswith(".py"):
            # Get the module name by removing the file extension
            module_name = file[:-3]

            # Create the fully-qualified module name by replacing path separators with dots
            module_path = os.path.join(root, file).replace(os.path.sep, ".")

            # Import the module dynamically and add it to the current namespace
            module = importlib.import_module(module_path)

            # Add the module to the current namespace (optional)
            globals()[module_name] = module

# Optionally, you can define __all__ to specify the modules to import when using `from package import *`
# For example:
# __all__ = ['module1', 'module2']