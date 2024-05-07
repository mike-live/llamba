from setuptools import find_packages, setup

setup(
    name='bioage_framework',
    packages=find_packages(include=['bioage_framework']),
    version='0.1.0',
    description='Library to merge BioAge models with LLMs',
    author='Sergei Tikhomirov',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.0'],
    test_suite='tests',
)