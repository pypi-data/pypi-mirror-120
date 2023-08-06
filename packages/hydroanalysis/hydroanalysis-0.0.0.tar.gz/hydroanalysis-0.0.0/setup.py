import setuptools
import os

setuptools.setup(
    name='hydroanalysis',
    version='0.0.0',
    author='Marco Dal Molin',
    author_email='marco.dalmolin.1991@gmail.com',
    description='Framework for calculating hydrological signatures',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       "README.md")).read(),
    long_description_content_type='text/markdown',
    url='https://hydroanalysis.readthedocs.io/en/latest/',
    license='LGPL',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',  # https://martin-thoma.com/software-development-stages/
    ],
    install_requires=[
        'numpy>=1.20.*',
        'pandas>=1.2.*',
    ],
)