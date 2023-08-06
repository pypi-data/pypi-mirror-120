import os
import setuptools
from setuptools import find_packages
# import CONSTANTS

requirements = "requirements.txt"
readme = "README.md"
# requirement_path = CONSTANTS.Requirements_path
readme_path = os.path.join(os.path.dirname(__file__), readme)


with open(readme, "r", encoding="utf-8") as fh:
    long_description = fh.read()

# with open(requirement_path) as f:
#     install_requires = f.read().splitlines()

setuptools.setup(
    name="demo_fa",
    version="0.0.1",
    author="Shreejaa Talla",
    author_email="shreejaa.talla@gmail.com",
    description="Solar Filaments data augmentation demo package",
    url="https://bitbucket.org/gsudmlab/bbso_fa/src/master/",
    project_urls={
        "Source": "https://bitbucket.org/gsudmlab/bbso_fa/src/master/",
    },
    packages = find_packages(where='bbsofa',exclude=['tests.*', 'tests', 'docs.*', 'docs']),
    package_data={
        '.': ['requirements.txt']},
    install_requires=[
        'pillow',
        'torchvision',
        'sortedcontainers',
        'opencv_python',
    ],
    py_modules=['CONSTANTS'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],

)

