import argparse


def main():
    parser = argparse.ArgumentParser(description='Forme Groups CLI & SDK')
    parser.add_argument('-b', '--arg2', help='Description of argument 2', required=False)

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()