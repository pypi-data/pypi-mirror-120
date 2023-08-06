import io
from setuptools import setup

from pathlib import Path

readme_path = Path(__file__).parent / "README.md"

with io.open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="section-index-optional",
    version="0.2.0",
    packages=["section_index_optional"],
    url="https://github.com/rkk1995/section-index-optional",
    license="MIT",
    author="Ravindu Kodippili",
    author_email="noreply@gmail.com",
    description="This plugin allows to configure section pages optionally.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["mkdocs"],
    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        "mkdocs.plugins": [
            "section-index-optional = section_index_optional:SectionIndexPlugin",
        ]
    },
)