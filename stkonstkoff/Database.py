import os
import io

class AWS_Static_Info:
    def __init__(self):
        pass

        self.aws_regions = {
            'us': {
                'us-east': ['us-east-1', 'us-east-2'],
                'us-west': ['us-west-1', 'us-west-2']
            },
            'asia': {
                'ap-east': ['ap-east-1'],
                'ap-south': ['ap-south-1'],
                'ap-northeast': ['ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3'],
                'ap-southeast': ['ap-southeast-1', 'ap-southeast-2']
            },
            'africa': {
                'af-south': ['af-south-1']
            },
            'canada': {
                'ca-central': ['ca-central-1']
            },
            'europe': {
                'eu-central': ['eu-central-1'],
                'eu-west': ['eu-west-1', 'eu-west-2', 'eu-west-3'],
                'eu-south': ['eu-south-1'],
                'eu-north': ['eu-north-1']
            },
            'middle_east': {
                'me-south': ['me-south-1']
            },
            'south_america': {
                'sa-east': ['sa-east-1']
            }
        }


class TemplateDB:
    def __init__(self):
        self.template_path = "data/cached_templates"
        self.templates_database = self.files_to_dict(self.template_path)


        self.valid_regions = [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'af-south-1',
            'ap-east-1', 'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3',
            'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1',
            'eu-west-2', 'eu-west-3', 'eu-south-1', 'eu-north-1', 'me-south-1', 'sa-east-1'
        ]
        self.valid_

    def files_to_dict(self, directory):
        """
        Takes a file path and returns a dictionary where the keys are file names
        and the values are the file contents.

        Args:
            directory (str): The path to the directory containing the files.

        Returns:
            dict: A dictionary mapping file names to their contents.
        """
        # Dictionary to store file names and contents
        files_dict = {}

        # Get a list of all files in the directory
        file_names = os.listdir(directory)

        # For each file in the directory
        for file_name in file_names:
            # Construct the full file path
            file_path = os.path.join(directory, file_name)

            # If this path is a file, read it and add to the dictionary
            if os.path.isfile(file_path):
                with io.open(file_path, 'r', encoding='utf-8') as f:
                    files_dict[file_name] = f.read()

        return files_dict

    def display_database(self, data=None):
        """
        Displays all key-value pairs in self.templates_database, numbered from 1 to n.
        """
        if data is None:
            data = self.templates_database
        for i, key in enumerate(data, start=1):
            print(f"{i}. {key}")

    # def get_template_content(self, template_name):
    #     if template_name is None:
    #         exit(print("db error 1"))
    #     contents = {}
    #     with io.open(self.templates_database, 'r', encoding='utf-8') as content:
    #         contents.append(content.readlines())
    #     return contents


# Very inefficient data handling....
# class DataHandler:
#     def __init__(self):
#         self.data_path = "data/"
#         self.template_cache = "../data/cached_templates/"
#         self.database = {
#             'name_template': {'stack-template.db': []},
#             'cached_maps': {'cached-configs.db': []},
#             'working_configurations': {'configs.db': []},
#             'template_paths': {'template_paths.db': []},
#             'prefix_strings': {'prefix_strings.db': []}
#         }
#         self.data_types = {
#             'name_template': 'dict',
#             'cached_maps': 'dict',
#             'working_configurations': 'list',
#             'template_paths': 'list',
#             'prefix_strings': 'list'
#         }
#
#     def get_data_format(self, data_type):
#         """
#         Returns the data format associated with a given data_type.
#         Args:
#             data_type (str): The data type/key.
#         Returns:
#             str: The associated data format ('dict' or 'list'), or None if data_type is not found.
#         """
#         return self.data_types.get(data_type)
#
#     def save_data(self, data, data_type, file_path):
#         """
#         Saves the data associated with a given data_type to a file.
#         Args:
#             data_type (str): The data type/key.
#             data (dict or list): The data to be saved.
#             file_path (str): The path to the file to save the data.
#         """
#         if isinstance(data, dict):
#             data_entry = Utilities.convert_to_list(data)
#         else:
#             data_entry = data
#
#         with open(file_path, 'a') as file:
#             if isinstance(data_entry, list):
#                 file.write('\n'.join(data_entry))
#             else:
#                 file.write(str(data_entry))
#             file.write('\n')
#
#     def load_settings_from_db(self):
#         for key, value in self.database.items():
#             data_file = list(value.keys())[0]
#             file_path = f"{self.data_path}/{data_file}"
#             data_format = self.data_types.get(key)
#
#             if data_format == 'list':
#                 with open(file_path, 'r') as file:
#                     data = file.read().splitlines()
#             elif data_format == 'dict':
#                 with open(file_path, 'r') as file:
#                     data = dict(line.split(':') for line in file.read().splitlines())
#             else:
#                 print("Invalid data format")
#                 continue
#
#             self.database[key] = data
#
#     def values_from_database(self, data_type, number_of_values):
#         """
#         Returns a specified number of values from a given data type.
#         Args:
#             data_type (str): The data type/key.
#             number_of_values (int): The number of values to return.
#         Returns:
#             dict or list: The values retrieved from the database.
#         """
#         data = self.database.get(data_type)
#         if isinstance(data, dict):
#             # If data is a dict, return the specified number of key-value pairs
#             return dict(list(data.items())[:number_of_values])
#         elif isinstance(data, list):
#             # If data is a list, return the specified number of items
#             return data[:number_of_values]
#         else:
#             print("Invalid data format")
#             return None
#
#     def insert_new_value(self, data_type, data_entry):
#         """
#         Inserts a new value into a given data type.
#         Args:
#             data_type (str): The data type/key.
#             data_entry (str or dict): The value to be inserted.
#         """
#         data = self.database.get(data_type)
#         if isinstance(data, dict):
#             if isinstance(data_entry, dict):
#                 data.update(data_entry)
#         elif isinstance(data, list):
#             if isinstance(data_entry, str):
#                 data.append(data_entry)
#         else:
