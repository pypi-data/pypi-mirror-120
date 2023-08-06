from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="concrete-hnumpy",
    version="0.0.10",
    author="zama",
    author_email="hello@zama.ai",
    description="Concrete hnumpy for the Concrete Framework",
    packages=("concrete.hnumpy",),
    namespace_packages=("concrete",),
    package_dir={"concrete.hnumpy": "hnumpy"},
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
