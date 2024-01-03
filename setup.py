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
    version="0.3",
    install_requires=install_requires("requirements.txt"),
    extras_require={
        "dev": install_requires("requirements-dev.txt"),
        "build": ["wheel"],
    },
    packages=find_packages(),
    include_package_data=True,
)
