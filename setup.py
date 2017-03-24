from setuptools import setup

setup(
    name="seriesly",
    version="0.7",
    description="Python client for seriesly database",
    author="Pavel Paulau",
    author_email="pavel.paulau@gmail.com",
    install_requires=[
        "requests==2.1.0",
        "decorator",
    ],
    packages=[
        "seriesly",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
