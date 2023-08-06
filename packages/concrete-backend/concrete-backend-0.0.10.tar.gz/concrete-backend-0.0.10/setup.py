from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="concrete-backend",
    version="0.0.10",
    author="zama",
    author_email="hello@zama.ai",
    description="Concrete backend for the Concrete Framework",
    packages=("concrete.backend",),
    namespace_packages=("concrete",),
    package_dir={"concrete.backend": "backend"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zama.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
