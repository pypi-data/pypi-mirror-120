import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptlibs",
    description="Support library for penterepTools",
    version="0.0.2",
    url="https://www.penterep.com/",
    author="Penterep",
    author_email="d.kummel@penterep.com",
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires = '>=3.6',
    install_requires=["requests"]
)