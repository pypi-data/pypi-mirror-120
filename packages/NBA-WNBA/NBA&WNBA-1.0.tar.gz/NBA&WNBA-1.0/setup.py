import setuptools
from pathlib import Path

setuptools.setup(
            name='NBA&WNBA',
            version = 1.0,
            long_description = Path('README.md').read_text(),
            packages = setuptools.find_packages(exclude=['Data','Tests'])
)