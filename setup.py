from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'linearstage==0.1.0',
        'max7219'
        ],
)