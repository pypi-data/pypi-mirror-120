from .commands import InitCommand, PublishCommand
from argparse import ArgumentParser
from . import __version__


class PKG:
    def __init__(self):
        self.parser = ArgumentParser(prog='pkg')
        self.parser.add_argument('--version', action='version', version=__version__)

        subparsers = self.parser.add_subparsers(dest='command')
        InitCommand(subparsers.add_parser('init', help='Create "package.json" file'))
        PublishCommand(subparsers.add_parser('publish', help='Publish package to PyPi'))

    def execute(self) -> None:
        args = self.parser.parse_args()
        if args.command is None:
            self.parser.parse_args(['-h'])
            return
        args.func(args)


def main():
    PKG().execute()


if __name__ == '__main__':
    main()
