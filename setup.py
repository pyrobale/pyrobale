from setuptools import setup, find_packages

setup(
    name="pyrobale",
    version="0.2.5",
    author="Ali Safamanesh",
    author_email="darg.q.a.a@gmail.com",
    description="A python wrapper for bale api",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pyrobale/pyrobale",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "requests",
    ],
)