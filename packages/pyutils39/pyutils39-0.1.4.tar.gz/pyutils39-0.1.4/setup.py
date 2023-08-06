import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutils39",
    version="0.1.4",
    author="Enderbyte09",
    author_email="enderbyte09@gmail.com",
    description="A utilities package",
    long_description=long_description,
    py_modules=['pyutils39'],
    long_description_content_type="text/markdown",
    url="https://github.com/Enderbyte-Programs/pyutils39",
    project_urls={
        "Bug Tracker": "https://github.com/Enderbyte-Programs/pyutils39/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)