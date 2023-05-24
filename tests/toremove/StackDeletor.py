import argparse
import boto3
import time
import os
from stkonstkoff.UserAuthentication import UserAccess

class StackDeletor:
    def __init__(self):
        self.user = UserAccess
        self.cf_client = boto3.client('cloudformation')


    def get_all_stack_names(self):
        response = self.cf_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
        stack_names = [stack['StackName'] for stack in response['StackSummaries']]
        return stack_names

    def delete_stack_by_number(self):
        stack_names = self.get_all_stack_names()
        self.print_list_with_numbers(stack_names)
        idx = int(input("Enter the number of the stack you want to delete: "))
        if 1 <= idx <= len(stack_names):
            self.delete_stack(stack_names[idx - 1])
        else:
            print('Invalid stack index.')

    def delete_stack(self, stack_name):
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack_status = response['Stacks'][0]['StackStatus']

            if stack_status == 'DELETE_COMPLETE':
                print(f'Stack "{stack_name}" is already deleted.')
                return

            self.cf_client.delete_stack(StackName=stack_name)
            print(f'Deleting stack "{stack_name}"...')

            while True:
                response = self.cf_client.describe_stacks(StackName=stack_name)
                stack_status = response['Stacks'][0]['StackStatus']

                if stack_status in ['DELETE_COMPLETE', 'DELETE_FAILED']:
                    break

                time.sleep(5)

            print(f'Stack "{stack_name}" deleted successfully.')

        except Exception as e:
            print(f'Failed to delete stack "{stack_name}":', str(e))

    @staticmethod
    def print_list_with_numbers(items):
        for i, item in enumerate(items, start=1):
            print(f"{i}.) {item}")

    def delete_all_stacks(self):
        stack_names = self.get_all_stack_names()
        for stack_name in stack_names:
            self.delete_stack(stack_name)

StackDeletor().delete_all_stacks()