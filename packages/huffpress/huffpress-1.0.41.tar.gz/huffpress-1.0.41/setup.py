import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="huffpress",
    version="1.0.41",
    author="Usman Ahmad",
    author_email="uahmad3013@outlook.com",
    description="Library containing Huffman algos and bespoke compressor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selphaware/huffpress",
    project_urls={
        "Bug Tracker": "https://github.com/selphaware/huffpress/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["tqdm==4.62.1"]
)
