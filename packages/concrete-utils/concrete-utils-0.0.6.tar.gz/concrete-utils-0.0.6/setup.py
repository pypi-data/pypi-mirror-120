import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concrete-utils",
    version="0.0.6",
    author="Zama Team",
    author_email="hello@zama.ai",
    description="Zama Concrete-utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zama.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
