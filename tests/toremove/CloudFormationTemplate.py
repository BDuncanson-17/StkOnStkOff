import os
import boto3
class CloudFormationTemplate:
    """
    Represents a CloudFormation template.

    Attributes:
        template_path (str): The path to the CloudFormation template file.
        template_name (str): The name of the template file.
        template_body (str): The content of the CloudFormation template.
        valid_template (bool): Indicates if the template is valid or not.
    """

    def __init__(self):
        """
        Initialize a CloudFormationTemplate object.

        Args:
            template_path (str): The path to the CloudFormation template file.
        """
        self._template_path = stkget_template_path()
        self._template_name = os.path.basename(template_path)
        self._template_body = self._load_template_body()
        self._valid_template = None

    @property
    def template_name(self):
        """Get the name of the template file."""
        return self._template_name

    @property
    def template_body(self):
        """Get the content of the CloudFormation template."""
        return self._template_body

    @template_body.setter
    def template_body(self, value):
        """Set the content of the CloudFormation template."""
        self._template_body = value
        self._valid_template = self._validate_template()

    @property
    def valid_template(self):
        """Check if the template is valid."""
        return self._valid_template

    def _load_template_body(self):
        """Load the content of the CloudFormation template from the file."""
        with open(self._template_path, 'r') as file:
            return file.read()

    def _validate_template(self):
        """
        Validate the CloudFormation template.

        Returns:
            bool: True if the template is valid, False otherwise.
        """
        try:
            cloudformation_client = boto3.client('cloudformation')
            response = cloudformation_client.validate_template(TemplateBody=self._template_body)
            return True
        except Exception as e:
            print(f"The template at '{self._template_path}' is invalid.")
            return False


template_dir = "/Users/bdunk/PycharmProjects/stkonstkoff/tests/infrastucture"
my_templates = []

for filename in os.listdir(template_dir):
    file_path = os.path.join(template_dir, filename)
    if os.path.isfile(file_path):
        my_templates.append(CloudFormationTemplate(file_path))

print(my_templates[0].template_name)  # Output: Template name of the first file in the directory
