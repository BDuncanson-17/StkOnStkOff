from UserAuthentication import UserAccess
from CloudFormations import CFStacks
from Utilities import Utilities
import argparse

_G_SESSION = UserAccess()
_cft = CFStacks()
_utils = Utilities()
_stkdel = _cft.StackDeletor()
_stkcreator = _cft.StackCreator()


def selection_delete(stacks_names=None):
    if all and lst:
        _stkdel.delete_all_stacks(lst)
    else:
        stacks = _cft.stack_names
        if not stacks:
            print("There are no active stacks")
        else:
            _utils.print_numbered_list(stacks)
            if len(stacks) == 1:
                _stkdel.delete_stack(stacks[0])
            else:
                all_stacks = _stkdel.all_or_select()
                if all_stacks:
                    _stkdel.delete_all_stacks()
                else:
                    _stkdel.delete_stack_by_number()


def selection_create(all=False, lst=None):
    if all and lst is not None:
        print("Creating all stacks...")
        _stkcreator.create_stacks(lst)
    else:
        print("Creating stack...")
        print("Not set up for individual stack creation.")


def selection_list_stack():
    stacks = _cft.stack_names
    if stacks:
        _utils.print_numbered_list(stacks)
    else:
        print("There are no active stacks")


def main():
    parser = argparse.ArgumentParser(description="Stack Management")
    subparsers = parser.add_subparsers(dest="command")

    delete_parser = subparsers.add_parser("delete", help="Delete stacks")
    delete_parser.add_argument("-a", "--all", action="store_true", help="Delete all stacks")
    delete_parser.add_argument("-l", "--list", nargs="*", help="Delete specified stacks")

    create_parser = subparsers.add_parser("create", help="Create stacks")
    create_parser.add_argument("-a", "--all", action="store_true", help="Create all stacks")
    create_parser.add_argument("-l", "--list", nargs="*", help="Create specified stacks")

    subparsers.add_parser("list", help="List stacks")

    args = parser.parse_args()

    if args.command == "delete":
        selection_delete(all=args.all, lst=args.list)
    elif args.command == "create":
        selection_create(all=args.all, lst=args.list)
    elif args.command == "list":
        selection_list_stack()
    pass

if __name__ == "__main__":
    main()

