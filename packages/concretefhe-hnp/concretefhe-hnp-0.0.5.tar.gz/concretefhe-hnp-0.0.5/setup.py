import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concretefhe-hnp",
    version="0.0.5",
    author="Zama Team",
    author_email="hello@zama.ai",
    description="Zama Concretefhe-hnp",
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
