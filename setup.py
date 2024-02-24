""" So that I can pip install the package
    and use the modules in notebooks
"""
import setuptools

setuptools.setup(
    name="analyze",
    version="0.0.1",
    description="A small example package",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
