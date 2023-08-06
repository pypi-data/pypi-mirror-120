import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aprheology",
    version="0.3.0",
    author="Kevin De Bruycker",
    author_email="kevindebruycker@gmail.com",
    description="Set of tools to easily analyse Anton Paar rheometer data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    license="MIT License",
    packages=setuptools.find_packages(),
    # package_data={'pymacroms': ['RawFileReader/Unix/*', 'RawFileReader/Windows/*'], },
    install_requires=["matplotlib", "numpy", "openpyxl", "pandas", "PySimpleGUI", "scipy", "statsmodels"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)