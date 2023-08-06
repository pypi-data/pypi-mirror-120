import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opsvis",
    version="0.94.3",
    author="Seweryn Kokot",
    author_email="sewkokot@gmail.com",
    description="OpenSeesPy (OpenSees) Python postprocessing and visualization module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sewkokot/ops_vis",
    packages=setuptools.find_packages(exclude=["tests", "tests.*",
                                               "README.md"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
