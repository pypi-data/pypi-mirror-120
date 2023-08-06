import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='videolytics',  
    version='0.1',
    scripts=['videolytics'] ,
    author="Samran Elahi",
    author_email="m.samranelahi@gmail.com",
    description="Efficiently process videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samran-Elahi/Videolytics",
    project_urls={
        "Bug Tracker": "https://github.com/Samran-Elahi/Videolytics/issues",
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