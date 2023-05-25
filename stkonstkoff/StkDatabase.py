import Utilities

data_path = "../data/"


# Very inefficient data handling....
class DataHandler:
    def __init__(self):
        self.data_path = "../data/"
        self.template_cache = "../data/cached_templates/"
        self.database = {
            'name_template': {'stack-template.db': []},
            'cached_maps': {'cached-configs.db': []},
            'working_configurations': {'configs.db': []},
            'template_paths': {'template_paths.db': []},
            'prefix_strings': {'prefix_strings.db': []}
        }
        self.data_types = {
            'name_template': 'dict',
            'cached_maps': 'dict',
            'working_configurations': 'list',
            'template_paths': 'list',
            'prefix_strings': 'list'
        }

    def get_data_format(self, data_type):
        """
        Returns the data format associated with a given data_type.
        Args:
            data_type (str): The data type/key.
        Returns:
            str: The associated data format ('dict' or 'list'), or None if data_type is not found.
        """
        return self.data_types.get(data_type)

    def save_data(self, data, data_type, file_path):
        """
        Saves the data associated with a given data_type to a file.
        Args:
            data_type (str): The data type/key.
            data (dict or list): The data to be saved.
            file_path (str): The path to the file to save the data.
        """
        if isinstance(data, dict):
            data_entry = Utilities.convert_to_list(data)
        else:
            data_entry = data

        with open(file_path, 'a') as file:
            if isinstance(data_entry, list):
                file.write('\n'.join(data_entry))
            else:
                file.write(str(data_entry))
            file.write('\n')

    def load_settings_from_db(self):
        for key, value in self.database.items():
            data_file = list(value.keys())[0]
            file_path = f"{self.data_path}/{data_file}"
            data_format = self.data_types.get(key)

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

    def insert_new_value(self, data_type, data_entry):
        """
        Inserts a new value into a given data type.
        Args:
            data_type (str): The data type/key.
            data_entry (str or dict): The value to be inserted.
        """
        data = self.database.get(data_type)
        if isinstance(data, dict):
            if isinstance(data_entry, dict):
                data.update(data_entry)
        elif isinstance(data, list):
            if isinstance(data_entry, str):
                data.append(data_entry)
        else:
            print("Invalid data format")
