import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='raspberrypi-python-tm1637',
    py_modules=['tm1637'],
    version='1.3.0',
    description='Raspberry Pi Python port from MicroPython library for TM1637 LED driver.',
    long_description='This library lets you operate quad 7-segment LED display modules based on the TM1637 LED driver with Raspberry PI.',
    keywords='tm1637 raspberry pi seven segment led python',
    url='https://github.com/lawerencem/raspberrypi-python-tm1637',
    author='Mike Causer',
    author_email='mcauser@gmail.com',
    maintainer='Lawerence E. Mize, Jr.',
    maintainer_email='lawerencem@gmail.com',
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
