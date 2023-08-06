import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "easylatex2image",
    version = "0.0.1",
    install_requires=["pdf2image"],
    author = "Martin Pflaum",
    author_email = "martin.pflaum.09.03.1999@gmail.com",
    description = "another latex converter 2 pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/martinpflaum/easylatex2image",
    keywords=["python","latex","image","png","jpg"],
    project_urls={
        "Bug Tracker": "https://github.com/martinpflaum/easylatex2image/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.6",
)