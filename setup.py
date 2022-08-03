import setuptools
from codecs import open
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = path.abspath(path.dirname(__file__))

# Get the required packages
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()
    
    
setuptools.setup(
    name='EquityLens',
    version='0.0.1',
    author='Wei Chen',
    author_email='victoriaweichen7@gmail.com',
    description='DEI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xie1027/EquityLens',
    project_urls = {
        "Bug Tracker": "https://github.com/xie1027/EquityLens/issues"
    },
    license='MIT',
    packages=['EquityLens'],
    #install_requires=['requests'],
)
