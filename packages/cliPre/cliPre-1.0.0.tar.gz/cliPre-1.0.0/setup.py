from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="cliPre",
    version="1.0.0",
    description="Command line preprocessing includes input dataset, data Description, handling Null Values, encoding, feature scaling and download the preprocessed data in csv format.",
    long_description_content_type="text/markdown",
    author="Yash",
    url="https://github.com/yashb007/CLI-Package",
    author_email="yyashpal_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["mypackage"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas',
                      'sklearn'
     ],
    #  entry_points={
    #     "console_scripts": [
    #         "cliProcessor=mypackage:main",
    #     ]
    #  },
)