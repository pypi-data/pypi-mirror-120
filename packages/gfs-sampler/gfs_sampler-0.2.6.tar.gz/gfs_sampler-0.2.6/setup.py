from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name = 'gfs_sampler',
    version = '0.2.6',
    author = 'Edwin Farley',
    author_email = 'edwin_farley@alumni.brown.edu',
    description = "Sample permutations of one data set with respect to another data set within defined blocks for the purposes of computing statistics over a merged data set.",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://pypi.org/project/gfs_sampler/',
    package_data={'' : ['LICENSE', 'df1.csv', 'df2.csv', 'df_full.csv']},
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    packages = find_packages(),
    install_requires = ['theano==1.0.4', 'pymc3==3.6'],
    python_requires = '>=3.6, <3.8'
)
