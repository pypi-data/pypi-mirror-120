from setuptools import setup, find_packages

setup(
    name='skinny-telegram-bot-wrapper',
    version='0.1.2',
    packages=find_packages(where='src'),
    license='MIT',
    python_requires='>=3.6, <4',
    install_requires=['flask', 'requests', 'requires'],
    package_dir={"": "src"}
)
