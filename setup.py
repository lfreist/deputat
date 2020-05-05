from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='deputat',
    version='1.0.0',
    description='deputat overview',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lfreist/deputat",
    author='lfreist',
    author_email='freist.leon@gmx.de',
    packages=['deputat', 'deputat/GUI/', 'deputat/GUI/pictures/'],
    package_dir={'deputat': ['GUI/pictures/*.svg']},
    install_requires=[
              'PyQt5',
              'distro',
              'openpyxl'
              ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)

