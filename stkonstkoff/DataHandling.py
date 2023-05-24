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

    def create_database(self):
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

