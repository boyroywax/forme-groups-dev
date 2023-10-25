import argparse
from groups import Groups
from groups.base import BaseContainer, BaseSchema
from groups.unit import GroupUnit, Credential, Data, Owner, Nonce


groups = Groups()


def main():
    parser = argparse.ArgumentParser(description='Forme Groups CLI & SDK')
    parser.add_argument('-b', '--beep', help='Description of argument 2', required=False)
    parser.add_argument('-c', '--create', help='Description of argument 3', required=False)

    args = parser.parse_args()
    print(args)
   
    if args.beep:
        print('beep')

    if args.create:
        print('create, {}'.format(args.create))
        data: Data = Data(BaseContainer((args.create), "tuple"))
        groups.controller._create_group_unit(data=data)
        print(groups.controller.active)
        # groups.save_state()


if __name__ == '__main__':
    main()
