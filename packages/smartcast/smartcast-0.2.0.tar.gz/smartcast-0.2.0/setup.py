import setuptools
import site

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

site.ENABLE_USER_SITE = True

setuptools.setup(
    name="smartcast",
    version="0.2.0",
    author="QHPEA",
    author_email="oss@qhpea.org",
    description="Recursively cast json to python dataclasses, typing, and class. Also provides reverse.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qhpea/smartcast",
    project_urls={
        "Bug Tracker": "https://github.com/qhpea/smartcast/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7,<3.10",
)
