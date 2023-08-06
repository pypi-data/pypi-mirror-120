from setuptools import setup, find_packages

setup(
    name='pysmarthome-govee',
    description='Govee plugin for pysmarthome',
    version='1.1.0',
    author='Filipe Alves',
    author_email='filipe.alvesdefernando@gmail.com',
    install_requires=[
        'govee_api2~=1.3.0',
        'pysmarthome~=3.0',
    ],
    packages=find_packages(),
    url='https://github.com/filipealvesdef/pysmarthome-govee',
    zip_zafe=False,
)
