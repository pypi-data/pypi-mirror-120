from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ncafs",
    version="0.1",
    description="Neighborhood Component Analysis Feature Selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["ncafs"],
    url="https://gitlab.com/pedro.paiva/ncafs",
    download_url="https://gitlab.com/pedro.paiva/ncafs/-/archive/v0.1/ncafs-v0.1.tar.gz",
    license="BSD 3-Clause",
    author="Pedro Paiva",
    author_email="paiva@ita.br",
    install_requires=[
        "scikit-learn>=0.23",
        "setuptools>=52.0.0",
        "numpy>=1.20",
        "scipy>=1.6",
        "pytest>=6.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research"
    ],
    python_requires=">=3.7"
)
