translationstring
=================

A library used by various `Pylons Project <http://pylonsproject.org>`_
packages for internationalization (i18n) duties related to translation.

This package provides a *translation string* class, a *translation
string factory* class, translation and pluralization primitives, and a
utility that helps `Chameleon <http://chameleon.repoze.org>`_
templates use translation facilities of this package.  It does not
depend on `Babel <http://babel.edgewall.org>`_, but its translation
and pluralization services are meant to work best when provided with
an instance of the ``babel.support.Translations`` class.

Please see http://docs.pylonsproject.org/projects/translationstring/dev/ or
the ``docs/index.rst`` file in this package for the documentation.
