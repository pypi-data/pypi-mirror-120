from setuptools import setup, find_packages

setup(
    name='libgen-py-api',
    version='1.0.3',
    packages=find_packages(where='src'),
    author='shrnemati',
    license='MIT',
    python_requires='>=3.6, <4',
    install_requires=['flask', 'requires', 'bs4', 'requests'],
    package_dir={"": "src"}
)
