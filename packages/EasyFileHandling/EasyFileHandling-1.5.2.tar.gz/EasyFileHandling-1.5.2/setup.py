import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyFileHandling",
    version="1.5.2",
    author="Haider Ali",
    author_email="",
    description="A simple and useful package for File Handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProjectsWithPython/FileHandling",
    project_urls={
        "Bug Tracker": "https://github.com/ProjectsWithPython/FileHandling/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['Pillow']
)