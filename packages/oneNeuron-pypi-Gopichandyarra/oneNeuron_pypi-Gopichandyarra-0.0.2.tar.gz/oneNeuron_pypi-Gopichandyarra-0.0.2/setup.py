import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

Project_name = "oneNeuron_pypi"
User_name = "Gopichandyarra"

setuptools.setup(
    name=f"{Project_name}-{User_name}",
    version="0.0.2",
    author="Gopichandyarra",
    author_email="Gopichandyarra.1@gmail.com",
    description="Its an implimentation of Perceptron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{User_name}/{Project_name}",
    project_urls={
        "Bug Tracker": f"https://github.com/{User_name}/{Project_name}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "tqdm"
    ]
)