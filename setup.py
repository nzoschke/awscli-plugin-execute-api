import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awscli_plugin_execute_api",
    version="0.0.1",
    author="Noah Zoschke",
    author_email="noah@mixable.net",
    description="Plugin to configure a single AWS CLI operation to invoke an API Gateway method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nzoschke/awscli-plugin-execute-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)