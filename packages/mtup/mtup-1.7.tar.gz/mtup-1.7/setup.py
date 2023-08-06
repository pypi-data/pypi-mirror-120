#setup.py
from setuptools import setup
import re

#change version number in mtup file  add/edit version="DESIRED_VERSION NUMBER" at the top of file

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('mtup').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"


setup(
    name='mtup',
    scripts=['mtup'],
    version= version,
    install_requires = ['pyclip'],
    description = 'upload file/folders through cli',
    long_description = long_descr,
    author = 'madhavth'
)
