import boto3
import subprocess
import os


class StackCreator:
    def __init__(self, template_directory="../../test/cft"):
        self.cf_client = boto3.client('cloudformation')
        self.template_files = []
        self.template_files = self.find_json_yaml_files(template_directory)
        self.template_map = None

    @staticmethod
    def prompt_prefix_string():
        add_prefix = str(
            input("Would you like to a prefix string to the stacks in your set like webpdf- (y/n):\n")).lower()
        if add_prefix == 'n' or add_prefix == 'no':
            return ""
        prefix_str = input("Add the string you want all your stacks to start with:\n")
        return prefix_str

    def create_stack_map(self, prefix_str=None):
        templates = self.template_files
        if templates is not None and len(templates) > 1:
            if len(self.template_files) == 0:
                return {}
            return {input("Enter the name of the stack:\n"): self.template_files[0]}

        stack_template_map = {}
        if prefix_str is None:
            prefix_str = self.prompt_prefix_string()

        num_stacks = int(input("Enter the number of stacks (1-20):\n"))
        for i in range(num_stacks):
            print(f"\nStack {i + 1}:")
            print("Select a template:")
            for j, template_name in enumerate(self.template_files):
                print(f"{j + 1}. {os.path.basename(template_name)}")

            selected_template_index = int(input("Enter the number corresponding to the template for stack {i}:\n"))
            if 1 <= selected_template_index <= len(self.template_files):
                selected_template = self.template_files[selected_template_index - 1]
                stack_name = input(f"Enter the stack name:\n{prefix_str}")
                stack_template_map[prefix_str + stack_name] = selected_template
            else:
                print("Invalid template selection. Skipping this stack.")

        return stack_template_map

    @staticmethod
    def find_json_yaml_files(directory):
        json_yaml_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.json', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    json_yaml_files.append(file_path)

        return json_yaml_files

    def add_tempate(template_path):
        template_path.template_files.append(template_path)

    @staticmethod
    def run_cft_lint(file_path):
        try:
            subprocess.check_output(['cft-lint', file_path])
            return True
        except subprocess.CalledProcessError:
            return False

    def create_stacks(self, stack_mapping):
        for stack_name, template_filepath in stack_mapping.items():
            try:
                with open(template_filepath, 'r') as template_file:
                    template_body = template_file.read()

                response = self.cf_client.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Capabilities=['CAPABILITY_NAMED_IAM'],  # Add this capability
                    OnFailure='ROLLBACK'  # Set the stack rollback behavior on failure
                )

                stack_id = response['StackId']
                print(f"Stack creation initiated. Stack ID: {stack_id}")

                print(f"Waiting for stack '{stack_name}' to be created...")
                waiter = self.cf_client.get_waiter('stack_create_complete')
                waiter.wait(StackName=stack_name)

                # After waiting, check the status of the stack
                stack_response = self.cf_client.describe_stacks(StackName=stack_name)
                stack_status = stack_response['Stacks'][0]['StackStatus']

                if stack_status == 'CREATE_COMPLETE':
                    print(f"Stack '{stack_name}' created successfully.")
                else:
                    print(f"Stack failed to complete due to event: {stack_status}")
                    break

            except Exception as e:
                print(f"Failed to create stack '{stack_name}': {str(e)}")
                break


s = StackCreator("../../tests")
s.create_stack_map()
print(s.template_files)