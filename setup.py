from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="2.2.6",
    packages=find_packages(),
    install_requires=[
        'stage>=0.3.0',
        'max7219'
        ],
)
