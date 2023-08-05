import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.in", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="drpg",
    version="2021.09.0",
    author="Grzegorz Janik",
    description="Download and keep up to date your purchases from DriveThruRPG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glujan/drpg",
    packages=["drpg"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["drpg=drpg.cmd:run"],
    },
    python_requires=">=3.8",
    install_requires=install_requires,
    package_data={"drpg": ["py.typed"]},
)
