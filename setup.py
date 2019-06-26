from setuptools import setup
import sdist_upip
import os
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='grown',
    version='0.1.0',
    packages=['picoweb'],
    url='https://github.com/SvenMatzke/userv',
    license='MIT',
    author='SvenMatzke',
    author_email='matzke.sven@googlemail.com',
    description='',
    long_description=README,
    cmdclass={'sdist': sdist_upip.sdist},
    install_requires=['userv', 'userv.async_server', 'micropython-ulogging']
)
