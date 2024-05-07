from setuptools import find_packages, setup

setup(
    name='bioage_framework',
    packages=find_packages(include=['bioage_framework']),
    version='0.1.0',
    description='Library to merge BioAge models with LLMs',
    author='Sergei Tikhomirov',
    install_requires=['requests', 'numpy', 'pandas', 'torch>=1.10.0', 'pytorch-lightning==1.6.4', 'scipy==1.10.1', 'omegaconf', 'scikit-learn>=1.1.3', 'shap'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.0'],
    test_suite='tests',
)