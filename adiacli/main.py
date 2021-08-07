import os
import sys

from easycli import Root, Argument


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class ADia(Root):
    __help__ = 'ASCII diagram language interpreter'
    __arguments__ = [
        Argument('-V', '--version', action='store_true'),
        Argument('--no-rstrip', action='store_true'),
        Argument(
            '-C', '--change-directory',
            default='.',
            help='Change the current working directory before executing, '
                 'default: ".".'
        ),
        Argument(
            'file',
            nargs='*',
            help='File containing adia source code. if not given, the '
                 'standard input will be used.'
        ),
    ]

    def __call__(self, args):
        import adia

        if args.version:
            print(adia.__version__)
            return

        outfile = sys.stdout

        def render(infile):
            adia.print(
                infile,
                outfile,
                rstrip=False if args.no_rstrip is True else False
            )

        if args.change_directory != '.':
            os.chdir(args.change_directory)

        try:
            if not args.file:
                render(sys.stdin)
            else:
                for index, filename in enumerate(args.file):
                    if index:
                        print(file=outfile)

                    with open(filename) as f:
                        render(f)

            return EXIT_SUCCESS
        except adia.InterpreterError as ex:
            print(ex, file=sys.stderr)
            return EXIT_FAILURE
