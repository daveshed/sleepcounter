from setuptools import setup, find_packages
setup(
    name="sleepcounter",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'linearstage==0.1.1',
        'max7219'
        ],
)