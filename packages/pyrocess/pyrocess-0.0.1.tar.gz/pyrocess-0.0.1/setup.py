from setuptools import setup
from pathlib import Path

ROOT = Path(__file__).parent

LONG_DESCRIPTION = (ROOT / 'README.md').read_text()

setup(
    name='pyrocess',
    version='0.0.1',
    description='Multiprocessing wrapper for Python',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Eder Lima',
    author_email='lima.eder101@gmail.com',
    keywords=['python', 'async', 'multiprocessing'],
    license='MIT',
    packages=[
        'pyrocess',
        'pyrocess/decorators',
        'pyrocess/process',
        'pyrocess/strategies',
    ],
)