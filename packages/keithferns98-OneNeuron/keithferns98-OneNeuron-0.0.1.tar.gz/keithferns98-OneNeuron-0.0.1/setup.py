import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keithferns98-OneNeuron",
    version="0.0.1",
    author="Keith",
    author_email="keithfernandes311@gmail.com",
    description="Perceptron package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keithferns98/OneNeuron_pypi",
    project_urls={
        "Bug Tracker": "https://github.com/keithferns98/OneNeuron_pypi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "tqdm"
        "logging"
    ]
)