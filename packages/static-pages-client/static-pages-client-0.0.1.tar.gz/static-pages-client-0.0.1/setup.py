import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="static-pages-client",
    version="0.0.1",
    author="Dorin Musteata",
    author_email="dorin.musteata@ebs-integrator.com",
    description="static-pages-client is a package that helps working with Static Pages API easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebs-integrator/static-pages-client",
    project_urls={
        "Bug Tracker": "https://github.com/ebs-integrator/static-pages-client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)