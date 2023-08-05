import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heybooster-toolkit",
    version="0.0.10",
    author="Heybooster",
    author_email="hey@heybooster.ai",
    description="Heybooster Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/hey-booster/heybooster-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/hey-booster/heybooster-toolkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
