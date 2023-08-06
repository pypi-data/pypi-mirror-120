import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

Project_Name="OneNeuron_pypi"
USER_NAME='Vani Bhatia'

setuptools.setup(
    name=f"{Project_Name}-{USER_NAME}",
    version="0.0.2",
    author="USER_NAME",
    author_email="vanibhatia13@gmail.com",
    description="It's an implementation of perceptron class and function for preparing the data,saving the model,create and save the plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{Project_Name}",
    project_urls={
        "Bug Tracker":f"https://github.com/{USER_NAME}/{Project_Name}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "tqdm",
        "matplotlib",
        "pandas",
        "joblib"
    ]
)
