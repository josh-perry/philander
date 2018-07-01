from setuptools import setup

setup(name='philander',
    version='0.1',
    description='LÖVE version selector',
    url='https://github.com/josh-perry/philander',
    author='Josh Perry',
    author_email='',
    license='MIT',
    packages=['philander'],
    install_requires=[
        "appdirs",
    ],
    entry_points = {
        'console_scripts': ['philander=philander:main'],
    },
    zip_safe=True)
