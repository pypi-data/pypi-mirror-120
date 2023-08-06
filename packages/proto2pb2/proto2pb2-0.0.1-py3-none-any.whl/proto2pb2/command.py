
from proto2pb2.converter import Converter
import argparse

class Proto2pb2Command:

    def __str__(self):
        return "Commandline tool for transpiling .proto files to _pb2.py files"

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='For transpiling .proto files to _pb2.py files')
        self.subparser = self.parser.add_subparsers(help='Subcommands')

        self.convert_subparser = self.subparser.add_parser('convert', help='convert files')
        self.convert_subparser.add_argument('--protopath', metavar='-d', type=str, nargs='?',
                                            required=True,
                                            help='path to directory containing .proto files')
        self.convert_subparser.add_argument('--pb2path', metavar='-p', type=str, nargs='?',
                                            default='./lib',
                                            help='output directory for _pb2.py files')
        self.convert_subparser.set_defaults(func=self.convert)

        #TODO: a function that validates syntax of proto files
        self.validate_subparser = self.subparser.add_parser('validate', help='validates .proto files')
        self.validate_subparser.add_argument('--fpath', metavar='-f', type=str, nargs='?',
                                            required=True,
                                            help='path to directory containing .proto files')
        self.validate_subparser.set_defaults(func=self.validate)

        self.args = self.parser.parse_args()
        self.args.func()

    def convert(self):
        converter = Converter(protopath=self.args.protopath, pb2path=self.args.pb2path)
        converter.start()

    def validate(self):
        print("Not implemented this functionality ye :P")

def main():
    obj = Proto2pb2Command()
    #import pdb; pdb.set_trace()
    #Proto2pb2Command().start()

if __name__ == '__main__':
    main()
