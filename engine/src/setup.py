from setuptools import setup, find_packages

setup(
    name='skadoosh',
    version='0.1',
    packages=['agent_portal','engine/src/api','engine/src/core'],
    url='www.skadoosh.in',
    license='Apache License 2.0',
    author='cackharot',
    author_email='cackharot@gmail.com',
    long_description='True virtual agent help',
    zip_safe=False,
    install_requires=['Flask', 'nltk'],
    data_files = [('engine/src/api',['engine/src/api/application.cfg']),
                  ('engine/src', ['engine/src/requirements.txt'])]
)
