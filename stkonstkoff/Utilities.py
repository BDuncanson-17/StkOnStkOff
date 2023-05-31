
def print_numbered_list(items):
    """
    Prints a numbered list of items.

    Args:
        items (list): The list of items to print.
    """
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")
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

def yes_or_no(question):
    while True:
        user_input = input(question + ' (yes/no): ').strip().lower()
        if user_input == 'yes':
            return True
        elif user_input == 'no':
            return False
        else:
            print("Please respond with 'yes' or 'no'.")
