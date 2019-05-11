from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="2.2.0",
    packages=find_packages(),
    install_requires=[
        'linearstage>=0.2.1',
        'max7219'
        ],
)