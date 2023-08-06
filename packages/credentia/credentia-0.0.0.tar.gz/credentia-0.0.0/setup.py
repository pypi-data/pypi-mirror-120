from setuptools import setup
from pathlib import Path
long_description = Path("./README.md").read_text()

setup(
  name='credentia',
  version='0.0.0',
  description='A simple credential manager.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='@JohnRForbes',
  packages=['credentia']
)
