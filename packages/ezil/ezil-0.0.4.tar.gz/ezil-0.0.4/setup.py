import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezil",
    version="0.0.4",
    author="Marek Derer",
    author_email="marek.derer@gmail.com",
    description="Ezil.me mining pool API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derki-source/py-ezil",
    project_urls={
        "Bug Tracker": "https://github.com/derki-source/py-ezil/issues",
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