from setuptools import find_packages, setup


def install_requires(file_name):
    """Given the file name, return a list of requirements
    Assumes the file is in the same directory as the setup.py
    """
    req = []
    with open(file=file_name, mode="r", encoding="utf-8") as f:
        req = [requirement for requirement in f]
    return req


setup(
    name="space-war-rl",
    install_requires=install_requires("requirements.txt"),
    extras_require={"dev": install_requires("requirements-dev.txt")},
    packages=find_packages(),
)
