#
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='yamlalchemy',
    version='0.1.2',
    description='YAMLAlchemy is a Python-based library to convert YAML to SQLAlchemy read-only queries.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ahmetonol/yamlalchemy',
    author='Ahmet Onol',
    author_email='onol.ahmet@gmail.com',
    license='MIT',
    packages=['yamlalchemy'],
    install_requires=[
        'PyYAML',
        'SQLAlchemy'
    ],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
