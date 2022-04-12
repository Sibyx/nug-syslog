from setuptools import setup

setup(
    name='nug-syslog',
    version='0.1.0',
    packages=['nug_syslog'],
    url='https://github.com/Sibyx/nug-syslog',
    license='GPLv3',
    author='Jakub Dubec',
    author_email='xdubec@stuba.sk',
    description='Simple syslog server based on the RFC5424',
    entry_points={
        'console_scripts': [
            "nug-syslog = nug_syslog.__main__:main",
        ]
    },
    install_requires=[
        'zeroconf==0.38.*',
    ],
)
