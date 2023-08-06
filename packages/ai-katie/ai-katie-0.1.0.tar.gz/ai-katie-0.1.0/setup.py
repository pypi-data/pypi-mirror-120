import setuptools
from typing import List
import os
import re

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def load_version():
    """ Loads a file content """
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "katie", "__init__.py"))
    with open(filename, "rt") as version_file:
        init_file = version_file.read()
        version = re.search(r"__version__ = '([0-9a-z.-]+)'", init_file).group(1)
        return version


setuptools.setup(name='ai-katie',
                 version=load_version(),
                 description='Utility things for Data Science and AI',
                 long_description=long_description,
                 author='danpeczek',
                 author_email='danpeczek@gmail.com',
                 url='https://github.com/danpeczek/ai-katie',
                 project_urls={
                     "Bug Tracker": "https://github.com/danpeczek/ai-katie/issues",
                 },
                 install_requires=["torch", "numpy"],
                 classifiers=[
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Science/Research',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                     'Topic :: Communications :: Email',
                     'Topic :: Scientific/Engineering :: Artificial Intelligence',
                     'Topic :: Scientific/Engineering :: Information Analysis'
                 ],
                 package_dir={"": "."},
                 packages=setuptools.find_packages(where="."),
                 python_requires=">=3.6"
                 )
