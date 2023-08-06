from setuptools import setup

setup(
    name='pydriveziead',
    version='1.3.1',
    author='ZSK',
    author_email='zshabkalieh@gmail.com',
    packages=['pydrive', 'pydrive.test'],
    url='https://github.com/zieadshabkalieh/pydriveziead',
    license='LICENSE',
    description='easy.',
    long_description=open('README.rst').read(),
    install_requires=[
        "google-api-python-client >= 1.2",
        "oauth2client >= 4.0.0",
        "PyYAML >= 3.0",
    ],
)
