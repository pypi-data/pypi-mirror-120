""" setup.py created according to https://packaging.python.org/tutorials/packaging-projects """

import setuptools #type:ignore

with open("README.md", "r") as fh:
    long_description: str = fh.read()

setuptools.setup(
    name="multiformats",
    version="0.0.0",
    author="hashberg",
    author_email="sg495@users.noreply.github.com",
    url="https://github.com/hashberg-io/multiformats",
    description="Python implementation of multiformats protocols.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[ # see https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    package_data={"": [],
                  "multiformats": ["multiformats/py.typed"],
                 },
    install_requires=[],
    include_package_data=True
)
