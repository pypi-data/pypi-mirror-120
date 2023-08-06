import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptthreads",
    description="ptthreads",
    version="0.0.5",
    url="https://www.penterep.com/",
    license="GPLv3+",
    author="Penterep",
    author_email="info@penterep.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires = '>=3.6',
    install_requires=["ptlibs"],
    long_description=long_description,
    long_description_content_type="text/markdown",   
)