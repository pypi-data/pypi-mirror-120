""" the magick behind ``pip install ...`` """
from setuptools import setup, find_packages


def get_long_description():
    """ returns contents of README.md file """
    with open("README.md", "r", encoding="utf8") as file:
        long_description = file.read()
    return long_description


setup(
    name='numba-mpi',
    url="https://github.com/atmos-cloud-sim-uj/numba-mpi",
    author='https://github.com/atmos-cloud-sim-uj/numba-mpi/graphs/contributors',
    version='0.3',
    setup_requires=['setuptools_scm'],
    license='GPL v3',
    description='Numba @njittable MPI wrappers tested on Linux, macOS and Windows',
    install_requires=('numba', 'numpy', 'mpi4py'),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=['numba_mpi', 'numba_mpi.*'])
)
