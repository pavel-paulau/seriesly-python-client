#
# Copyright 2012, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import setuptools
from setuptools import setup

setup(
    name="seriesly",
    version="0.3.2",
    description="Python client for seriesly database.",
    author="Couchbase, Inc.",
    author_email="pavel.paulau@gmail.com",
    install_requires=["requests==1.0.4", "decorator"],
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
