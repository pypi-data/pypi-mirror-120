import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AlteMatrix",
    version="0.0.1",
    author="Ayomide Ayodele-Soyebo",
    author_email="midesuperbest@gmail.com",
    description="This tool lets you perform some quick tasks for CTFs and Pentesting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ir0n-c0d3X/AlteMatrix",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "altematrix"},
    packages=setuptools.find_packages(where="altematrix"),
    python_requires=">=3.6",
    include_package_data=True,
)
