from setuptools import setup
import sdist_upip


setup(
    name='grown',
    version='0.0.21-dev',
    packages=['grown'],
    url='https://github.com/SvenMatzke/grown',
    license='MIT',
    author='SvenMatzke',
    author_email='matzke.sven@googlemail.com',
    description='Grown server to run tasks',
    long_description=open('README.rst').read(),
    cmdclass={'sdist': sdist_upip.sdist},
    install_requires=['userv', 'userv.async-server', 'micropython-ulogging']
)
