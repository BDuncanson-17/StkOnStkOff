from stkonstkoff import AWSUserAuthorization
import boto3


def main():

    user_auth = AWSUserAuthorization()
    int cnt = 0
    while not user_auth.check_aws_credentials()and cnt < 4:
        user_auth.set_aws_credentials()
        cnt+=1

    boto3.sessions.client('cloudformations')
    print("Currently you have the following stacks")

    input("woud you like to create or delete stacks?")







if __name__ == "__main__":
