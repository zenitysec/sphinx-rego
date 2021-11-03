from setuptools import setup, find_packages

setup(
    name="sphinx-rego",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "docutils"
    ],
    url="https://github.com/zenitysec/sphinx-rego",
    license="MIT",
    author="Zenity",
    author_email="join@zenity.io",
    description="A sphinx extension that automatically documents Open Policy Agent Rego policies using the rego_metadoc property. Maintained by Zenity, learn more at https://zenity.io.",
    long_description="""A sphinx extension that automatically documents Open Policy Agent Rego policies using the rego_metadoc property.\nFor installation and usage details, see https://github.com/zenitysec/sphinx-rego.\nMaintained by Zenity, learn more at https://zenity.io.""",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation"
    ],
)