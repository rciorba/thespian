from setuptools import setup, find_packages


def get_dependencies(filename):
    dependencies = []
    with open("REQUIREMENTS") as f:
        dependencies = f.read().splitlines()
    return dependencies

setup(
    name="thespian",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=get_dependencies("REQUIREMENTS"),
    package_data={
        '': ['*.txt'],
    },
    # metadata for upload to PyPI
    author="Radu Ciorba",
    author_email="radu.ciorba@3pillarglobal.com",
    description="Multiprocessing based Actor Model",
    url="http://github.com/rciorba/thespian",
)
