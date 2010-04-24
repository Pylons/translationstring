import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = []

setup(name='translationstring',
      version='0.1',
      description=('Utility library for i18n relied on by various Repoze '
                   'packages'),
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Topic :: Software Development :: Internationalization",
          "Topic :: Software Development :: Localization",
          ],
      keywords='i18n l10n internationalization localization gettext chameleon',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-like (http://repoze.org/license.html)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = requires + ['Babel'],
      install_requires = requires,
      test_suite="translationstring",
      )

