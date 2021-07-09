from setuptools import setup, find_packages

setup(
    name="sphinx-rego",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "docutils"
    ],
    url="https://github.com/zenitysec/sphinx-rego",
    license="MIT",
    author="Zenity",
    author_email="join@zenity.io",
    description="A sphinx extension that automatically documents Open Policy Agent Rego policies using the _rego_metadoc_ property.",
    long_description="""A sphinx extension that automatically documents Open Policy Agent Rego policies using the _rego_metadoc_ property. For installation and usage details, see https://github.com/zenitysec/sphinx-rego.""",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation"
    ],
)