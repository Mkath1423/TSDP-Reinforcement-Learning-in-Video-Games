import argparse


# Create the parser
parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
parser.add_argument('config',
                    type=str,
                    default=None,
                    nargs="?",
                    help='the global config')

args = vars(parser.parse_args())


def get_arg(arg: str):
    return args.get(arg, None)


if __name__ == "__main__":
    print(args)