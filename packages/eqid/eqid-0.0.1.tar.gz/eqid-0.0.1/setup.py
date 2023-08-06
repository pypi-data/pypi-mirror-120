import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eqid",
    version="0.0.1",
    author="Steve Lukis",
    author_email="stevelukis88@gmail.com",
    description="Python package to retrieve the most recent earthquake information in Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevelukis/eqid/",
    project_urls={
        "Blog": "https://medium.com/@stevelukis",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4==4.10.0',
        'requests==2.26.0',
    ],
    python_requires=">=3.6",
)
