from .cloudformations.CloudFormations import CFStacks

from stkonstkoff.cloudformations.CloudFormations import StackCreator
from stkonstkoff.cloudformations.CloudFormations import StackDeletor
from stkonstkoff.UserAuthentication import UserAccess
from stkonstkoff.Utilities import Utilities


_SESSION = UserAccess()
cft = CCFStacks()
def main():
    Utilities.print_numbered_list(cft.get_stack_names())


if __name__ == "__main__":
    main()

# import argparse
#
# parser = argparse.ArgumentParser()
#
# subparsers = parser.add_subparsers(dest="command")
#
# # Create parser for "a_command"
# parser_a = subparsers.add_parser("a_command", aliases=["a", "acmd"])
# parser_a.add_argument("-x")
#
# # Create parser for "b_command"
# parser_b = subparsers.add_parser("b_command", aliases=["b", "bcmd"])
# parser_b.add_argument("-y")
#
# args = parser.parse_args()
#
# if args.command in ["select", "s", "acmd"]:
#     print(f"Running 'a_command' with x = {args.x}")
# elif args.command in ["b_command", "b", "bcmd"]:
#     print(f"Running 'b_command' with y = {args.y}")
