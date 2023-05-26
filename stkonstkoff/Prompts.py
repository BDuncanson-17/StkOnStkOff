import re
import os
import boto3
from stkonstkoff import Data


class Prompts:

# Usage
lower_bound = 1
upper_bound = 20
aws_stack_name = Prompts.validate_aws_stack_name('MyStackName')
num = Prompts.validate_number_between_bounds('21', lower_bound, upper_bound)
response = Prompts.validate_yes_no('yes')
filename = Prompts.validate_filename('myfile.yaml')

print(aws_stack_name)
print(num)
print(response)
print(filename)
