#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

long_description = """
The Alarm Listener Server is a Python 3 project for receiving alarm notifications.

----

%s

----

Run the server with::

    $ python3 -m alarmlistener

""" % readme


setup(
    name='AlarmListenerServer',
    version='1.0',
    description='The Alarm Listener Server is a project for receiving alarm notifications.',
    long_description=long_description,
    author='Miel Donkers',
    author_email='miel.donkers@gmail.com',
    url='https://github.com/mdonkers/AlarmListener',
    packages=find_packages(exclude=["*.tests", "tests"]),
    install_requires=['requests', 'sqlalchemy', 'Jinja2', 'setuptools'],
    tests_require=['nose'],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'alarmlistener = alarmlistener.server:run',
            ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Home Automation',
        'Topic :: Security',
        ],
    )
