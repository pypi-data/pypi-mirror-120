from setuptools import setup, find_packages
from io import open
from os import path

import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

README_CONTENT = (CURRENT_DIR / "README.md").read_text()

with open(path.join(CURRENT_DIR, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='smalldocpy',
    description='A small Python code parser which allow to generate a basic documentation',
    version='0.0.1',
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    python_requires='>=3',
    entry_points='''
[console_scripts]
smalldoc=smalldoc.__main__:main
    ''',
    author="Jean-Pascal Thiery",
    keywords="documentation",
    long_description=README_CONTENT,
    long_description_content_type="text/markdown",
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    url='https://github.com/jpthiery/smalldoc',
    dependency_links=dependency_links,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ]
)
