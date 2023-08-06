import setuptools

setuptools.setup(
    name="parsingresumes",
    version="0.0.1",
    author="Mansi Shah",
    author_email="mshah@choosefreedomit.com",
    description="A package to wrap all the parsing of Sovern resume JSONs",
    packages=['parsing_resumes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)