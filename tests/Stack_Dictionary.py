import os


def generate_stack_names(template_directory):
    template_files = os.listdir(template_directory)
    templates_in_dir = 3#######
    stack_mapping = {}
    if templates_in_dir == 0:
        print("No template files found in the directory.")
        return {}
    num_stacks = int(input("Enter the number of stacks you want to build: "))
    int cnt = 0;
    while cnt < num_stacks:
        print("Select a template file:")
        for i, file in enumerate(template_files, start=1):
            print(f"{i}. {file}")

        selected_template_index = input("Which template file would you like to use(select number)\n: ")
        if selected_template_index < 1 or selected_template_index > templates_in_dir:
            print("Select a template file:")
        else:
            stack_mapping[template_files[selected_template_index-1]] = None
            cnt = cnt + 1

    selected_template_file = template_files[selected_template_index - 1]
    selected_template_path = os.path.join(template_directory, selected_template_file)




    stack_mapping = {}

    for i in range(num_stacks):
        stack_name = input(f"Enter the stack name for Stack-{i + 1}: ")
        stack_mapping[stack_name] = selected_template_path

    return stack_mapping


# Example usage
template_directory = '/home/bryan/Documents/stkonstkoff/tests/infrastucture'
stack_mapping = generate_stack_names(template_directory)
print(stack_mapping)
