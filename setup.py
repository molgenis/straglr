from setuptools import setup

setup(
    name='straglr',
    #remove version here because the setuptools refuses the postfix
    description='Straglr',
    long_description='Short tandem repeat genotyping using long reads',
    url='https://github.com/bcgsc/straglr.git',
    author='Readman Chiu',
    author_email='rchiu@bcgsc.ca',
    license='BCCA',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        ],
    packages=['straglr'],
    install_requires = [
        'pysam==0.22.1',
        'pybedtools==0.10.0',
        'numpy==1.26.4',
        'pathos==0.3.3',
        'scikit-learn==1.5.2',
        'scipy==1.14.1',
        'natsort==8.4.0'
        ],
    entry_points ={
        'console_scripts': [
            'straglr-genotype=straglr.straglr_genotype:main'
        ]
    }
)
