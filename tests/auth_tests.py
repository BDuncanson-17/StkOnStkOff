import boto3

# Create IAM client
iam = boto3.client('iam')

# Get list of all users
users = iam.list_users()
user_list = users['Users']

# Iterate over each user
for user in user_list:
    user_name = user['UserName']
    print(f"\nUser: {user_name}")

    # Get attached user policies
    user_policies = iam.list_attached_user_policies(UserName=user_name)
    if user_policies['AttachedPolicies']:
        print("Attached Policies:")
        for policy in user_policies['AttachedPolicies']:
            print(f"  PolicyName: {policy['PolicyName']}, PolicyArn: {policy['PolicyArn']}")
    else:
        print("No attached policies.")
