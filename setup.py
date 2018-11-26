from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        'linearstage==0.0.0',
        'max7219'
        ],
)