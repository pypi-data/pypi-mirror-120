import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="simple-flask-cms",
    version="0.0.2",
    description="A minimal CMS for flask",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mousetail/simple-flask-cms",
    author="Maurits van Riezen (mousetail)",
    author_email="mousetail+pypi@mousetail.nl",
    license="GPL-2",
    classifiers=[

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=["simple_flask_cms"],
    include_package_data=True,
    install_requires=["flask", "markdown", "flask_sqlalchemy"],
)
