import boto3
import regions as regions

from stkonstkoff.__inti__ import DEFAULT_SESSION

aws_regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'af-south-1', 'ap-east-1', 'ap-south-1',
               'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1',
               'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-south-1', 'eu-west-3', 'eu-north-1',
               'me-south-1', 'sa-east-1']


class CloudFormationStacks:
    def __init__(self, session=DEFAULT_SESSION):
        self._regions = regions
        self._selected_region = None
        self._region_stack_names = {}
        self._cf_permissions = None
        self._cf_stacks = None
        self._cf_templates = None

    @property
    def selected_region(self):
        return self._selected_region

    @selected_region.setter
    def selected_region(self, region):
        if region in self._regions:
            self._selected_region = region
            self._cf_client = boto3.client("cloudformation", region_name=region)
            self._update_stack_names()
        else:
            print("Invalid region. Please select a valid AWS region.")

    def _update_stack_names(self):
        response = self._cf_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
        stack_names = [stack['StackName'] for stack in response['StackSummaries']]
        self._region_stack_names[self._selected_region] = stack_names

    @property
    def cf_stacknames(self):
        return self._region_stack_names

    # ... other methods of the class ...


# Example usage
stacks = CloudFormationStacks()
stacks.selected_region = 'us-east-1'
print(stacks.cf_stacknames)
