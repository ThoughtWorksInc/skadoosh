from setuptools import setup, find_packages

setup(
    name='skadoosh.core',
    version='0.1',
    packages=find_packages(),
    url='www.skadoosh.in',
    license='Apache License 2.0',
    author='cackharot',
    author_email='cackharot@gmail.com',
    long_description='True virtual agent help',
    zip_safe=False,
    install_requires=['Flask', 'nltk']
)
