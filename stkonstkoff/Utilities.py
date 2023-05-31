
def print_numbered_list(items):
    """
    Prints a numbered list of items.

    Args:
        items (list): The list of items to print.
    """
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")

def ask_for_choice(items):
    """
    Displays a numbered list of items and asks the user to choose one.

    Args:
        items (list): The list of items to choose from.

    Returns:
        The chosen item.
    """
    while True:
        print_numbered_list(items)
        try:
            choice = int(input("Enter the number of your would like to delete: "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            elif choice == 'all':
                return items
            else:
                print(f"Please enter a number between 1 and {len(items)} or all\n")
        except ValueError:
            print("Please enter a valid number.\n")

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
