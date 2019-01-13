from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
        'linearstage==0.2.0',
        'max7219'
        ],
)