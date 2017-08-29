translationstring
=================

A library used by various `Pylons Project <https://pylonsproject.org>`_ packages
for internationalization (i18n) duties related to translation.

This package provides a *translation string* class, a *translation string
factory* class, translation and pluralization primitives, and a utility that
helps `Chameleon <https://chameleon.readthedocs.io/en/latest/>`_ templates use
translation facilities of this package.  It does not depend on `Babel
<http://babel.pocoo.org/en/latest/>`_, but its translation and pluralization
services are meant to work best when provided with an instance of the
``babel.support.Translations`` class.

Please see https://docs.pylonsproject.org/projects/translationstring/en/latest/
for the documentation.
