import os
import subprocess


strings = {
    "get_prefix": [
        "Would you like to add a prefix string to all of you stacks (y/n):\n",
        "Add the string you want all your stacks to start with: "
    ],
    "num_of_stacks": [
        "Enter the number of stacks you want to create(1-20): "
        "Invalid input. Enter the number of stacks you want to create(1-20 or q to quit):"
        ]
}

class StringUtilities:
    def __init__():
        strings = {
            "get_prefix": [
                "Would you like to add a prefix string to all of you stacks (y/n):\n",
                "Add the string you want all your stacks to start with: "
            ],
            "num_of_stacks": [
                "Enter the number of stacks you want to create(1-20): "
                "Invalid input. Enter the number of stacks you want to create(1-20 or q to quit):"
            ]
            
        }

    def yes_no_prompt(msg=):
        if msg is None:
            msg = "Yes or No?:  "
        yes_or_no = str(input(msg)).tolower
        return yes_or_no == "y" or yes_or_no == "yes"
    
    def get_string()
        if msg = None:
            msg = "Enter your value: "
        if validate then
            validate_range(
         return str(input(msg))
class Utilities:
    def __init__(self):
        self.data_path = "../data"

        pass

    @staticmethod
    def get_template_path():
        """
        Returns the absolute file system path for the relative path '../data/templates'.
        Returns:
            str: The absolute file system path.
        """
        relative_path = "../data/templates/"
        absolute_path = os.path.abspath(relative_path)
        return absolute_path

    @staticmethod
    def print_numbered_list(lst):
        """
        Prints the objects of a list on separate lines with numbered formatting.
        Args:
            lst (list): The list of objects to print.
        """
        for i, item in enumerate(lst, 1):
            print(f"{i}. {item}")

    @staticmethod
    def print_numbered_dict(dictionary):
        """
        Prints a dictionary with numbered items, one key-value pair per row.
        Args:
            dictionary (dict): The dictionary to print.
        """
        for i, (key, value) in enumerate(dictionary.items(), 1):
            print(f"{i}. {key}: {value}")

    def run_cft_lint(file_path):
        try:
            subprocess.check_output(['cft-lint', file_path])
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_file_name(file_path):
        """
        Returns the file name (including extension) from a given absolute file path.
        Args:
            file_path (str): The absolute file path.
        Returns:
            str: The file name (including extension).
        """
        if file_path == "":
            return ""
        return os.path.basename(file_path)

    @staticmethod
    def list_of_files_in_path(file_paths):
        file_names = []
        if len(file_paths) == 0:
            return file_names
        else:
            file_names = []
            for file in file_paths:
                file_names.append(Utilities.get_file_name(file))
        return file_names

    def find_json_yaml_files(self):
        json_yaml_files = []

        for root, dirs, files in os.walk(self.template_dir):
            for file in files:
                if file.endswith(('.json', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    json_yaml_files.append(file_path)

        return json_yaml_files

    @staticmethod
    def get_number_input(self, msg=None):
        if msg is None:
            msg = "Enter the number of stacks you would like to create(1-20):\n"
        return input(int(msg))

    @staticmethod
    def get_string_input(msg=None, template="", prefix_str=" "):
        if msg is None:
            msg = f"Enter the stack name of the stack for {template}:\n" \
                  f"{prefix_str}"
        return input(msg)

    @staticmethod
    def create_stack_map(dataobj, prefix_str=None, self=None):
        if not isinstance(dataobj, list):
            return {}
        if len(template_lst) == 0:
            return {}

        stack_template_map = {}
        if prefix_str is None:
            prefix_str = self.prompt_prefix_string()

        num_stacks = Utilities.get_number_input()
        for i in range(num_stacks):
            print(f"\nStack {i + 1}:")
            print("Select a template:")
            for j, template_name in enumerate(self.template_files):
                print(f"{j + 1}. {os.path.basename(template_name)}")

            selected_template_index = int(input(f"Enter the number corresponding to the template for stack {i + 1}:\n"))
            if 1 <= selected_template_index <= len(self.template_files):
                selected_template = self.template_files[selected_template_index - 1]
                stack_name = input(f"Enter the stack name:\n{prefix_str}")
                stack_template_map[prefix_str + stack_name] = selected_template
            else:
                print("Invalid template selection. Skipping this stack.")

        return stack_template_map

    @staticmethod
    def prompt_prefix_string():
        print(f"Would you like to add a prefix string that starts each stack name(Example: webpdf-)")
        add_prefix = input("(y/n):\t \n").lower()
        if add_prefix == 'n' or add_prefix == 'no':
            return ""
        return input("Enter the prefix string")
