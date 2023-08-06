from setuptools import setup, find_packages
from integration_tools import __version__

setup(
    name='smart-integration-tools',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pytz>=2018.4',
        'six>=1.11.0',
        'pycrypto==2.6.1',
        'smart-manage-crypt',
        'boto3',
    ],
    python_requires='>=3.7',
)
