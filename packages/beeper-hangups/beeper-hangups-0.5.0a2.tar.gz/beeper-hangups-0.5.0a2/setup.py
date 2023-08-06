from setuptools import setup
import os
import sys


if sys.version_info < (3, 6):
    raise RuntimeError("hangups requires Python 3.6+")


# Find __version__ without import that requires dependencies to be installed:
exec(open(os.path.join(
    os.path.dirname(__file__), 'hangups/version.py'
)).read())


with open('README.rst') as f:
    readme = f.read()


# Dependencies should be specified as a specific version or version range that
# is unlikely to break compatibility in the future. This is required to prevent
# hangups from breaking when new versions of dependencies are released,
# especially for end-users (non-developers) who use pip to install hangups.
install_requires = [
    'aiohttp>=3.7,<4',
    'async-timeout>=2,<4',
    'appdirs>=1.4,<1.5',
    'ReParser==1.4.3',
    'protobuf>=3.1.0,<3.17',
]

dev_install_requires = [
    "aiohttp_socks>=0.6,<0.7",
]

ui_install_requires = [
    'ConfigArgParse>=0.11.0,<2',
    'readlike>=0.1.2,<0.2',
    'urwid>=1.3.1,<2.2',
]


setup(
    name='beeper-hangups',
    version=__version__,
    description=('the first third-party instant messaging client for Google '
                 'Hangouts'),
    long_description=readme,
    url='https://github.com/beeper/hangups',
    author='Tom Dryer',
    author_email='tomdryer.com@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Communications :: Chat',
        'Environment :: Console :: Curses',
    ],
    packages=['hangups', 'hangups.ui'],
    install_requires=install_requires,
    extras_require={
        "dev": dev_install_requires,
        "ui": ui_install_requires,
    },
    entry_points={
        'console_scripts': [
            'hangups=hangups.ui.__main__:main',
        ],
    },
)
