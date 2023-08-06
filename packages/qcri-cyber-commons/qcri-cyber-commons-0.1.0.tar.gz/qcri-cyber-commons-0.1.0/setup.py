import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qcri-cyber-commons",
    version="0.1.0",
    long_description_content_type="text/markdown",
    url="https://github.com/qcri/Common",
    project_urls={
        "Bug Tracker": "https://github.com/qcri/Common/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
