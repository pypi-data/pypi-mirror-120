import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dune_analytics_fix",
    version="0.0.7",
    author="Justin Martin",
    author_email="justin@jmart.me",
    description="An interface for querying Dune Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/git-alice/dune-analytics",
    project_urls={
        "Bug Tracker": "https://github.com/git-alice/dune-analytics/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['gql[aiohttp]==2.0.0'],
)
