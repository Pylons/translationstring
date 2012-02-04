import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    README = ''
    CHANGES = ''

setup(name='translationstring',
      version='1.0',
      description=('Utility library for i18n relied on by various Repoze '
                   'and Pyramid packages'),
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.5",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Internationalization",
          "Topic :: Software Development :: Localization",
          ],
      keywords='i18n l10n internationalization localization gettext chameleon',
      author="Chris McDonough, Agendaless Consulting",
      author_email="pylons-discuss@googlegroups.com",
      url="http://pylonsproject.org",
      license="BSD-like (http://repoze.org/license.html)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="translationstring",
      )

