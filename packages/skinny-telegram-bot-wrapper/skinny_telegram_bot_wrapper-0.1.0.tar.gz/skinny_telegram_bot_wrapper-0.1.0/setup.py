from setuptools import setup, find_packages

setup(
    name='skinny_telegram_bot_wrapper',
    version='0.1.0',
    packages=find_packages(where='src'),
    license='MIT',
    python_requires='>=3.6, <4',
    install_requires=['flask', 'requests'],
    package_dir={"": "src"}
)
