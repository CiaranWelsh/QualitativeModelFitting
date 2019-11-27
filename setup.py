from setuptools import setup

MAJOR = 0
MINOR = 0
MICRO = 2

version = f'{MAJOR}.{MINOR}.{MICRO}'

setup(
    name='QualitativeModelFitting',
    version=version,
    packages=['qualitative_model_fitting'],
    license='MIT',
    long_description=open('README.md').read(),
    author='Ciaran Welsh',
    author_email='ciaran.welsh@newcastle.ac.uk',
    url='https://github.com/CiaranWelsh/QualitativeModelFitting',
    keywords=['SBML', 'antimony', 'tellurium', 'qualitative modelling'],
    install_requires=[
        'tellurium', 'pycotools3', 'pandas', 'numpy'
    ]
)
