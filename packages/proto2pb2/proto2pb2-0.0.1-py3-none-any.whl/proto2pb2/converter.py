import os, subprocess
from pathlib import Path
from pprint import pprint

from colorama import Fore


class Converter():
    SETUP_CONTENT = '''
import setuptools

setuptools.setup(
    name="{name}",
    version="0.0.1",
    author="me",
    author_email="me@example.com",
    description="Knowlegde graph apis",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)
'''
    GENERATE_COMMAND = 'python -m grpc_tools.protoc -I{proto_dir} --python_out={pb2path} {protofile}'
    PROTO_EXTENSION = '.proto'
    PY_EXTENSION = '.py'

    def __init__(self, protopath, pb2path='./lib'):
        self.protopath = protopath
        #TODO: make it work with proper python library structure where pb2path = pb2path/pb2path
        self.pb2path = pb2path #os.path.join(pb2path, os.path.basename(os.path.normpath(pb2path)))
        self.pythonpath = os.path.abspath(pb2path)

    def _get_files_with_suffix(self, root_dir, suffix):
        '''
        Return a dictionary of the following type:
        [{'../../myrepo/protos/keyvaluestore/keyvaluestore.proto': {'parent_path': '../../myrepo/protos/keyvaluestore'}},
         {'../../myrepo/protos/helloworld/helloworld.proto': {'parent_path': '../../myrepo/protos/helloworld'}},
         {'../../myrepo/protos/auth_sample/auth_sample.proto': {'parent_path': '../../myrepo/protos/auth_sample'}},
         {'../../myrepo/protos/route_guide/route_guide.proto': {'parent_path': '../../myrepo/protos/route_guide'}}]
        '''
        files = list()
        for root, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(suffix):
                    files.append( {os.path.join(root, filename): {'parent_path': root}} )
        return files

    def _get_pb2_dirs(self, protofiles):
        for filename in protofiles:
            for key, value in filename.items():
                value['pb2path'] = os.path.join(self.pb2path, value['parent_path'].removeprefix(self.protopath))
        return protofiles

    def _create_pb2_dirs(self, protofiles):
        #getting all unique directory names
        dirs = set()
        for f in protofiles:
            for key, value in f.items(): dirs.add(value['pb2path'])

        for d in dirs:
            if not os.path.exists(d):
                print("{}mkdir {}".format(Fore.YELLOW, d))
                os.makedirs(d)
            else:
                print("{}mkdir: {}: File exists".format(Fore.GREEN, d))
        return dirs

    def _generate(self, protofiles):
        for p in protofiles:
            for f, d in p.items():
                command = self.GENERATE_COMMAND.format(protofile=f,
                                                        proto_dir=self.protopath,
                                                        pb2path=self.pb2path,
                                                )
                run = subprocess.run(command.split(), capture_output=True)

                if run.returncode == 0:
                    pass
                    #print("{}Sucessfull: {}".format(Fore.GREEN, command))
                else:
                    print("{}Failed: {}".format(Fore.RED, command))
                    print(Fore.RED + run.stderr.decode('utf-8'))
                    print(Fore.RED + run.stdout.decode('utf-8'))

    def _create_init_files(self):
        for root, dirnames, filenames in os.walk(self.pythonpath):
            init_file = open(os.path.join(root, '__init__.py'), 'w+')
            for filename in filenames:
                if not filename.startswith('_') and filename.endswith('.py'):
                    import_line = 'from . import {}\n'.format(filename.split('.py')[0])
                    init_file.write(import_line)
            for dirname in dirnames:
                if not dirname.startswith('_'):
                    import_line = 'from . import {}\n'.format(dirname)
                    init_file.write(import_line)
            init_file.close()

    '''
    def _create_init_file(self):
        py_files = self._get_files_with_suffix(self.pb2path, '.py')
        pythonpaths = list()

        # get relative paths to modules in root python dir
        for filename in py_files:
            for key, value in filename.items():
                abs_path = os.path.abspath(key)
                abs_parent_path = os.path.abspath(value['parent_path'])
                common_path = os.path.commonprefix([Path(self.pythonpath).absolute(), abs_parent_path])
                module_path = abs_path.removeprefix(common_path)
                module_path = ((module_path.removeprefix('/')).replace('/', '.')).removesuffix('.py')
                if not module_path.endswith('__init__'): pythonpaths.append(module_path)
        # write to __init__.py
        init_file = open(os.path.join(self.pythonpath, '__init__.py'), 'w+')
        for p in pythonpaths: init_file.write('import {}\n'.format(p))
        init_file.close()

        return pythonpaths
    '''

    def _create_setup_file(self):
        setup_file = open(os.path.join(self.pythonpath, 'setup.py'), 'w+')
        lines = self.SETUP_CONTENT.format(name=os.path.basename(os.path.normpath(self.pythonpath)))
        setup_file.write(lines)

    def _echo_PYTHONPATHS(self, pb2_dirs):
        paths = self.pythonpath + ':'
        for _dir in pb2_dirs:
            paths = paths + os.path.abspath(_dir) + ':'
        print("Run the following command to use output directory as a module: {}export PYTHONPATH=$PYTHONPATH:{}".format(Fore.GREEN, paths))

    def start(self):
        protofiles = self._get_files_with_suffix(self.protopath, self.PROTO_EXTENSION)
        protofiles = self._get_pb2_dirs(protofiles)
        pb2_dirs = self._create_pb2_dirs(protofiles)
        self._generate(protofiles)
        self._create_init_files()
        self._create_setup_file()
        #self._echo_PYTHONPATHS(pb2_dirs)
