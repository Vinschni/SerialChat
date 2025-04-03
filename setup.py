from setuptools import setup, find_packages

setup(
    name="SerialChat",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'pyserial>=3.0',
        'pycryptodome'
    ],
)