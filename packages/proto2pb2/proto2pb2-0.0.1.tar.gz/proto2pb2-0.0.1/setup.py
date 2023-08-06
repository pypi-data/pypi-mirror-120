from setuptools import setup
from setuptools import find_packages

setup(
    name="proto2pb2",
    version="0.0.1",
    description="Uses protoc to convert a given directory of .proto files to _pb2.py files",
    keywords="proto2pb2",
    author="https://github.com/supriyopaul",
    author_email="paul.supriyo.paul@gmail.com",
    url="",
    license="MIT",
    dependency_links=["https://github.com/supriyopaul/proto2pb2"],
    install_requires=[
        "grpcio==1.39.0",
        "grpcio-tools==1.39.0",
        "protobuf==3.17.3",
        "six==1.16.0",
        "argparse==1.4.0",
        "colorama==0.4.4",
    ],
    package_dir={"proto2pb2": "proto2pb2"},
    packages=find_packages("."),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"console_scripts": ["proto2pb2 = proto2pb2:main"]},
)
