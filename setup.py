import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tunehelper", 
    version="0.0.1",
    author="archwisp",
    author_email="archwisp@gmail.com",
    description="Analyze engine logfiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/archwisp/TuneHelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, <3.0',
)
