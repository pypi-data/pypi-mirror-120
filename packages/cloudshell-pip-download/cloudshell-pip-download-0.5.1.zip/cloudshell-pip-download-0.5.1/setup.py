from setuptools import find_packages, setup


def read_file(file_name):
    with open(file_name) as f:
        return f.read().strip()


setup(
    name="cloudshell-pip-download",
    version=read_file("version.txt"),
    description="downloads python packages for specified platform and python version",
    author="Kyrylo Maksymenko",
    author_email="saklar13@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["pip-download = pip_download.cli:cli"]},
    include_package_data=True,
    install_requires=[
        "click~=8.0",
        "pip-tools~=6.2",
        "pip>=20.3,<22",
        "tqdm~=4.53",
        "packaging>=20.4,<22",
    ],
    python_requires="~=3.7",
)
