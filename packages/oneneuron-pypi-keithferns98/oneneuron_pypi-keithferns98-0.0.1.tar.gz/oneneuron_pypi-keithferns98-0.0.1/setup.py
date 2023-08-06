import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

Project_Name="oneneuron_pypi"
User_Name="keithferns98"
setuptools.setup(
    name=f"{Project_Name}-{User_Name}",
    version="0.0.1",
    author="User_Name",
    author_email="keithfernandes311@gmail.com",
    description="Perceptron package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keithferns98/oneneuron_pypi",
    project_urls={
        "Bug Tracker": "https://github.com/keithferns98/oneneuron_pypi/issues",
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