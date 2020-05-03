from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='deputat',
    version='0.2.1',
    description='deputat overview',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lfreist/deputat",
    author='lfreist',
    author_email='freist.leon@gmx.de',
    packages=[],
    install_requires=[
              'PyQt5',
              ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)

