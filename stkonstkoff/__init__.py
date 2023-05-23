import argparse
import boto3
import time
import os


def check_aws_credentials():
    try:
        session = boto3.Session()
        session.client('sts').get_caller_identity()
    except Exception as e:
        print("Failed to check AWS credentials:", str(e))
        exit(1)


def get_all_stack_names():
    cf_client = boto3.client('cloudformation')
    response = cf_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    stack_names = [stack['StackName'] for stack in response['StackSummaries']]
    return stack_names

def check_aws_credentials():
    try:
        session = boto3.Session()
        session.client('sts').get_caller_identity()
    except Exception as e:
        print("Failed to check AWS credentials:", str(e))
        exit(1)


def get_all_stack_names():
    cf_client = boto3.client('cloudformation')
    response = cf_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    stack_names = [stack['StackName'] for stack in response['StackSummaries']]
    return stack_names


def delete_stack_by_number(stack_names):
    print_list_with_numbers(stack_names)
    idx = int(input("Enter the number of the stack you want to delete: "))
    if 1 <= idx <= len(stack_names):
        delete_stack(stack_names[idx - 1])
    else:
        print('Invalid stack index.')


def delete_stack(stack_name):
    cf_client = boto3.client('cloudformation')
    try:
        response = cf_client.describe_stacks(StackName=stack_name)
        stack_status = response['Stacks'][0]['StackStatus']

        if stack_status == 'DELETE_COMPLETE':
            print(f'Stack "{stack_name}" is already deleted.')
            return

        cf_client.delete_stack(StackName=stack_name)
        print(f'Deleting stack "{stack_name}"...')

        while True:
            response = cf_client.describe_stacks(StackName=stack_name)
            stack_status = response['Stacks'][0]['StackStatus']

            if stack_status in ['DELETE_COMPLETE', 'DELETE_FAILED']:
                break

            time.sleep(5)

        print(f'Stack "{stack_name}" deleted successfully.')

    except Exception as e:
        print(f'Failed to delete stack "{stack_name}":', str(e))


def print_list_with_numbers(items):
    for i, item in enumerate(items, start=1):
        print(f"{i}.) {item}")


def delete_all_stacks():
    stack_names = get_all_stack_names()
    for stack_name in stack_names:
        delete_stack(stack_name)



def find_files_with_cft_lint(directory):
    json_yaml_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') or file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                if run_cft_lint(file_path):
                    json_yaml_files.append(file_path)

    return json_yaml_files


def run_cft_lint(file_path):
    try:
        subprocess.check_output(['cft-lint', file_path])
        return True
    except subprocess.CalledProcessError:
        return False

def get_template_body(template_source):
    with open(template_source, 'r') as template_file:
        template_body = template_file.read()
        return template_body
    return False






def main():
    parser = argparse.ArgumentParser(description='AWS CloudFormation stack management script')

    # Optional argument to specify AWS CLI credentials
    parser.add_argument('-c', '--credentials', help='Path to AWS CLI credentials file')

    # Add a mutually exclusive group for the other arguments that require AWS credentials
    group = parser.add_mutually_exclusive_group(required=True)

    # Argument to list all stack names
    group.add_argument('-l', '--list_all', action='store_true', help='List all stack names')

    # Argument to delete a specific stack
    group.add_argument('-d', '--delete_stack', nargs='?', const='select', help='Delete stack by index')

    # Argument to delete all stacks
    group.add_argument('-da', '--delete_all', action='store_true', help='Delete all stacks')

    args = parser.parse_args()

    # Check if AWS credentials are provided
    if args.credentials:
        boto3.setup_default_session(profile_name=args.credentials)

    # Check if AWS credentials are valid
    check_aws_credentials()

    # Execute the selected action
    if args.list_all:
        stack_names = get_all_stack_names()
        print_list_with_numbers(stack_names)

    if args.delete_stack:
        stack_names = get_all_stack_names()

        if args.delete_stack == 'select' or args.delete_stack == '':
            delete_stack_by_number(stack_names)
        else:
            idx = int(args.delete_stack)
            if 1 <= idx <= len(stack_names):
                stack_name = stack_names[idx - 1]
                delete_stack(stack_name)
            else:
                print('Invalid stack index.')
        exit()
    if args.delete_all:
        delete_all_stacks()


if __name__ == '__main__':
    main()
