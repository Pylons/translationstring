translationstring
=================

2.0 (unreleased)
----------------

- Add support for Python 3.8 - 3.13.

- Drop support for Python 2.7 and Python 3 < 3.8 (this release now adds
  ``python_requires='>=3.8'``, so that older Python versions won't install
  it.

- Remove ``translationstring.compat`` module.

1.4 (2020-07-09)
----------------

- Drop support for Python 2.6, 3.2 and 3.
- Update license classifiers


1.3 (2014-11-05)
----------------

- Fix Python 3-specific test failures.

- Restore compatibility with Python 3.2.

1.2 (2014-11-04)
----------------

- Add support for message contexts.

- If the object passed to a TranslationStringFactory ``__call__`` method is
  itself a translation string, use the passed object's ``domain`` instead of
  the domain passed to the factory's contstructor.  See
  https://github.com/Pylons/translationstring/pull/12 .


1.1 (2012-02-08)
----------------

- Add MANIFEST to make sure all files are present in a release. This fixes
  `ticket 8 <https://github.com/Pylons/translationstring/issues/8>`_.


1.0 (2012-02-04)
----------------

- coerce non-string values to a string during translation, except for None.

- Honour mapping information passed to the translator, combining it with
  mapping data already part of the translation string.
  
- Support formatting of translation strings with %-operator.

0.4 (09-22-2011)
----------------

- Python 3 compatibility (thanks to Joe Dallago, GSOC student).

- Remove testing dependency on Babel.

- Moved to GitHub (https://github.com/Pylons/translationstring).

- Added tox.ini for testing purposes.

0.3 (06-25-2010)
----------------

- Preserve default translations even if they are an empty string. This
  fixes problems with Chameleon being unable to determine if a translation
  is present or not.

0.2 (04-25-2010)
----------------

- Add ``__getstate__`` and ``__reduce__`` methods to translation
  string to allow for pickling.

- Fix bug in ChameleonTranslate.  When ``i18n:translate`` was used in
  templates, a translation string was inappropriately created with a
  ``default`` value of the empty string.  Symptom: template text would
  "disappear" rather than being returned untranslated.

0.1 (04-24-2010)
----------------

- Initial release.
