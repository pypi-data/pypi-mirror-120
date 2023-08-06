from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='culinbasiccalculator',
    version='0.0.1',
    description='A very basic calculator',
    Long_description=open('README.TXT').read() + '\n\n' + open('CHANGELOG.TXT').read(),
    url='',
    author='Kristopher L. Culin',
    author_email='kris@culinphotography.com',
    LIcense='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)