import os
import sys
import subprocess



class DataHandler:
    def __init__(self):
        self.data_path = "../data"
        self.database = {
            'template_name_map': {'stack-template-map.db': {}},
            'cached_maps': {'cached-configs.db': {}},
            'working_configurations': {'configs.db': {}},
            'template_paths': {'template_paths.db': []},
            'prefix_strings': {'prefix_strings.db': []}
        }
        self.datatypes = get_data_format

    def get_data_format(self, data_type):
        """
        Returns the data format associated with a given data_type.
        Args:
            data_type (str): The data type/key.
        Returns:
            str: The associated data format ('dict' or 'list'), or None if data_type is not found.
        """
        return type(self.database[data_type].value)

    def save_data(self, data_type, data):
        """
        Saves the data associated with a given data_type to a file.
        Args:
            data_type (str): The data type/key.
            data (dict or list): The data to be saved.
        """
        data_format = self.get_data_format(data_type)

        file_path = f"{self.data_path}/{list(data_format.keys())[0]}"

        if data_format[list(data_format.keys())[0]] == 'list':
            with open(file_path, 'w') as file:
                file.write('\n'.join(data))
        else:
            with open(file_path, 'w') as file:
                for key, value in data.items():
                    line = f"{key}:{value}\n"
                    file.write(line)

    def load_settings_from_db(self):
        for key, value in self.data_types.items():
            data_file = list(value.keys())[0]
            file_path = f"{self.data_path}/{data_file}"
            data_format = value[data_file]

            if data_format == 'list':
                with open(file_path, 'r') as file:
                    data = file.read().splitlines()
            elif data_format == 'dict':
                with open(file_path, 'r') as file:
                    data = dict(line.split(':') for line in file.read().splitlines())
            else:
                print("Invalid data format")
                continue

            self.database[key] = data


    def values_from_database(self, data_type, number_of_values):

            """
            Creates a dictionary from a file where each line represents a dictionary entry in the format 'key:value'.
            Args:
                settings_type (str): The path to the file to read.
            Returns:
                dict: The dictionary created from the file.
            """

    def values_from_database(self, data_type, number_of_values):
        """
        Returns a specified number of values from a given data type.
        Args:
            data_type (str): The data type/key.
            number_of_values (int): The number of values to return.
        Returns:
            dict or list: The values retrieved from the database.
        """
        data = self.database.get(data_type)
        if isinstance(data, dict):
            # If data is a dict, return the specified number of key-value pairs
            return dict(list(data.items())[:number_of_values])
        elif isinstance(data, list):
            # If data is a list, return the specified number of items
            return data[:number_of_values]
        else:
            print("Invalid data format")
            return None


class StkOnStkOffUtlities:

    def __init__(self):
        self.data_path = "../data"

        pass
    @staticmethod
    def create_dictionary_file(data, data_path="../data/", save_type=None,):
        """
        Creates a text file with each line representing a dictionary entry in the format 'key:value'
        if data is a dictionary. If data is a string, each line represents a separate entry.
        Args:
            data (dict or str): The data to write to the file.
            file_path (str): The path to the file to create.
        """
        stack_maps[]
    @staticmethod
    def get_template_path():
        """
        Returns the absolute file system path for the relative path '../test/cft/'.
        Returns:
            str: The absolute file system path.
        """
        relative_path = "../test/cft/"
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
                file_names.append(StkOnStkOffUtlities.get_file_name(file))
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
    def get_string_input(msg=None, template="", prefix_str =" "):
        if msg is None:
            msg = f"Enter the stack name of the stack for {template}:\n" \
                  f"{prefix_str}"
        return input(msg)
    @staticmethod
    def create_stack_map(template_lst, prefix_str=None, self=None):
        if isinstance(obj, dict):
            return template_lst
        if len(template_lst) == 0:
            return {}

        stack_template_map = {}
        if prefix_str is None:
            prefix_str = self.prompt_prefix_string()

        num_stacks = StkOnStkOffUtlities.get_number_input()
        for i in range(num_stacks):
            print(f"\nStack {i + 1}:")
            print("Select a template:")
            for j, template_name in enumerate(self.template_files):
                print(f"{j + 1}. {os.path.basename(template_name)}")

            selected_template_index = int(input(f"Enter the number corresponding to the template for stack {i+1}:\n"))
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


