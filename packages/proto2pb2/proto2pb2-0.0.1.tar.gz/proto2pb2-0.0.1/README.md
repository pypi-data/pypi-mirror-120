# proto2pb2
Generates "_pb2" files out of a given repo containing ".proto" files

## Prerequisites
```
Python >= 3.6
```

## Installation

### Download the source code
```bash
git clone https://github.com/supriyopaul/proto2pb2.git
cd proto2pb2/
```

### Install & activate a virtualenv
```bash
pip3 install virtualenv
virtualenv -p python3 ./test-env
source test-env/bin/activate
```

### Install `proto2pb2` tool
```bash
pip install .
```

## Usage
### Help
```bash
$ proto2pb2 -h
usage: proto2pb2 [-h] {convert,validate} ...

For transpiling .proto files to .py files

positional arguments:
  {convert,validate}  Subcommands
    convert           convert files
    validate          validates .proto files

optional arguments:
  -h, --help          show this help message and exit
```

```bash
$ proto2pb2 convert --help
usage: proto2pb2 convert [-h] --protopath [-d] [--pythonpath [-p]]

optional arguments:
  -h, --help         show this help message and exit
  --protopath [-d]   path to directory containing .proto files
  --pythonpath [-p]  output directory for python files
```

### Compile files
```bash
$ proto2pb2 convert --protopath ./protos/ --pb2path ./output
```

### Test
```bash
$ tree ./protos/
./protos/
├── auth_sample
│   └── auth_sample.proto
├── hellostreamingworld
│   └── hellostreamingworld.proto
├── helloworld
│   └── helloworld.proto
├── keyvaluestore
│   └── keyvaluestore.proto
└── route_guide
    └── route_guide.proto


$ tree ./output/
./output/
├── auth_sample
│   ├── auth_sample_pb2.py
│   └── auth_sample_pb2_grpc.py
├── hellostreamingworld
│   ├── hellostreamingworld_pb2.py
│   └── hellostreamingworld_pb2_grpc.py
├── helloworld
│   ├── helloworld_pb2.py
│   └── helloworld_pb2_grpc.py
├── keyvaluestore
│   ├── keyvaluestore_pb2.py
│   └── keyvaluestore_pb2_grpc.py
└── route_guide
    ├── route_guide_pb2.py
    └── route_guide_pb2_grpc.py
```

