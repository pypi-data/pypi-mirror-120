from setuptools import setup, find_packages

with open("requirements.txt") as f:
    req = f.read().splitlines()

setup(
    name="cse.py",
    version="1.1.1",
    description="An asynchronous Google Search Engine API wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hype3808/cse.py",
    author="Hype3808",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="google-api-wrapper, google, chrome-search-engine, cse",
    packages=find_packages(),
    install_requires=req,
    packagers=['cse']
)
