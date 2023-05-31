class Conversion:
    @staticmethod
    def convert_dictionary_to_list(dictionary):
        """
        Converts a dictionary into a list of key-value string representations.
        Args:
            dictionary (dict): The dictionary to convert.
        Returns:
            list: The resulting list of key-value pairs in string format.
        """
        result = []
        for key, value in dictionary.items():
            entry = f"{key}: {value}"
            result.append(entry)
        return result
    def convert_dictionary_to_list(dictionary):
        """
        Converts a dictionary into a list of key-value string representations.
        Args:
            dictionary (dict): The dictionary to convert.
        Returns:
            list: The resulting list of key-value pairs in string format.
        """
        result = []
        for key, value in dictionary.items():
            entry = f"{key}: {value}"
            result.append(entry)
        return result

class Printing:
    def __init__(self):
        """
        Initializer method. Currently does nothing.
        """
        pass

    def process_data(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(key, str) and isinstance(value, str):
                    print(f"Key: {key}, Value: {value}")
        elif isinstance(data, list):
            for element in data:
                if isinstance(element, str):
                    print(element)
        else:
            print(ErrorHander.cls_strings[0])

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
    def print_data_structure(data_type):
        """
        Prints a dictionary with numbered items, one key-value pair per row.
        Args:
            dictionary (dict): The dictionary to print.
        """
        for i, (key, value) in enumerate(dictionary.items(), 1):
            print(f"{i}. {key}: {value}")

    @staticmethod
    def run_cft_lint(file_path):
        """
        Runs the cft-lint tool on a given file.
        Args:
            file_path (str): The path to the file to lint.
        Returns:
            bool: True if linting succeeds, False otherwise.
        """
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
        """
        Returns a list of file names from a given list of file paths.
        Args:
            file_paths (list): List of file paths.
        Returns:
            list: The list of file names.
        """
        if len(file_paths) == 0:
            return []
        else:
            file_names = []
            for file in file_paths:
                file_names.append(Utilities.get_file_name(file))
        return file_names

    def find_json_yaml_files(self):
        """
        Returns a list of JSON/YAML file paths in the 'template_dir' directory.
        Returns:
            list: The list of JSON/YAML file paths.
        """
        json_yaml_files = []

        for root, dirs, files in os.walk(self.template_dir):
            for file in files:
                if file.endswith(('.json', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    json_yaml_files.append(file_path)

        return json_yaml_files

    @staticmethod
    def get_number_input(msg=None):
        """
        Prompts the user for a number input.
        Args:
            msg (str, optional): The prompt message.
        Returns:
            int: The user's input.
        """
        if msg is None:
            msg = "Enter the number of stacks you would like to create(1-20):\n"
        return int(input(msg))

    @staticmethod
    def get_string_input(msg=None):
        """
        Prompts the user for a string input.
        Args:
            msg (str, optional): The prompt message.
        Returns:
            str: The user's input.
        """
        if msg is None:
            return ""
        return input(msg)

    @staticmethod
    def yes_no(user_input):
        """
        Checks if the user's input starts with a 'y' or 'Y'.
        Args:
            user_input (str): The user's input.
        Returns:
            bool: True if the input starts with 'y' or 'Y', False otherwise.
        """
        return 'y' == user_input[0].lower()

    @staticmethod
    def stack_map(template_lst, prefix_str=None):
        """
        Maps stacks to their corresponding templates based on user input.
        Args:
            template_lst (list): The list of templates.
            prefix_str (str, optional): An optional prefix for stack names.
        Returns:
            dict: A dictionary mapping stack names to their corresponding templates.
        """
        if len(template_lst) == 0:
            return {}

        stack_template_map = {}
        if prefix_str is None:
            prefix_str = Utilities.prompt_prefix_string()

        num_stacks = Utilities.get_number_input()
        for i in range(num_stacks):
            print(f"\nStack {i + 1}:")
            print("Select a template:")
            for j, template_name in enumerate(template_lst):
                print(f"{j + 1}. {os.path.basename(template_name)}")

            selected_template_index = int(input(f"Enter the number corresponding to the template for stack {i + 1}:\n"))
            if 1 <= selected_template_index <= len(template_lst):
                selected_template = template_lst[selected_template_index - 1]
                stack_name = input(f"Enter the stack name:\n{prefix_str}")
                stack_template_map[prefix_str + stack_name] = selected_template
            else:
                print("Invalid template selection. Skipping this stack.")

        return stack_template_map

    @staticmethod
    def prompt_prefix_string():
        """
        Prompts the user for a prefix string.
        Returns:
            str: The user's input.
        """
        msg = PROMPTS["prefix"][0]
        msg1 = PROMPTS["prefix"][1]
        msg2 = PROMPTS["prefix"][2]
        print(msg)
        if Utilities.yes_no(input(msg1)):
            return Utilities.get_string_input(msg2)
        else:
            return ""


PROMPTS = {
    "prefix": [f"Would you like to add a prefix string that starts each stack name(Example: webpdf-)",
               "(y/n):\t",
               "Enter the prefix string:"]
}
