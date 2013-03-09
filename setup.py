from setuptools import setup

setup(
    name="seriesly",
    version="0.3.5",
    description="Python client for seriesly database.",
    author="Couchbase, Inc.",
    author_email="pavel.paulau@gmail.com",
    install_requires=["requests==1.0.4", "decorator", "ujson"],
    setup_requires=[],
    tests_require=[],
    url="http://www.couchbase.com/",
    license="LICENSE",
    keywords=["encoding", "i18n", "xml"],
    packages=["seriesly"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
