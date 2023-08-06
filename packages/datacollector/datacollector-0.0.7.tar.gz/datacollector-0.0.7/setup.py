from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.7' 
DESCRIPTION = 'PubMed article data collector'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
# with open('README.md', 'r') as rm:
#     LONG_DESCRIPTION = rm.read()
# LONG_DESCRIPTION = 'PubMed article data collector is able to let you download the metadata of bioinformatic acticle from the PubMed repository.'

# Setting up
setup(
        name="datacollector", 
        version=VERSION,
        author="Kwok Sun Cheng",
        author_email="<kwoksuncheng@unomaha.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=['beautifulsoup4', 'metapub', ], 
        keywords=['python', 'PubMed', 'Data collector'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)