from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='fairmaterials',
    version='0.0.210',
    keywords=['FAIRification','PowerPlant','Engineering'],
    description='Build a json file based on FAIRification standard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://engineering.case.edu/centers/sdle/',
    author='Roger French(ORCID:000000-0002-6162-0532), Liangyi Huang(ORCID:0000-0003-0845-3293), Will Oltjen(ORCID:0000-0003-0380-1033),Arafath Nihar, Jiqi Liu(ORCiD: 0000-0003-2016-4160), Justin Glynn, Kehley Coleman',
    author_email='roger.french@case.edu, lxh442@case.edu, wco3@case.edu,axn392@case.edu,jxl1763@case.edu,jpg90@case.edu, kac196@case.edu',
    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD License (BSD-3)',
    packages=find_packages(),
    
)