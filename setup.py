import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="31",
    version="1.5",
    author="Kavi Gupta",
    author_email="31@kavigupta.org",
    description="Runs code in a specified environment in the background and notifies you when it is done.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/31",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["31=s31.main:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=["attrs>=20.1.0", "display-timedelta==1.1", "filelock==3.0.12"],
)
