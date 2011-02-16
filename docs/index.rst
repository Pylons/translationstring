translationstring
=================

A library used by various `Pylons Project <http://pylonsproject.org>`_
packages for internationalization (i18n) duties.

This package provides a :term:`translation string` class, a
:term:`translation string factory` class, translation and
pluralization primitives, and a utility that helps :term:`Chameleon`
templates use translation facilities of this package.  It does not
depend on :term:`Babel`, but its translation and pluralization
services are meant to work best when provided with an instance of the
:class:`babel.support.Translations` class.

.. toctree::
   :maxdepth: 2

   tstrings.rst
   translation.rst
   pluralization.rst
   chameleon.rst
   api.rst
   glossary.rst

Index and Glossary
==================

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
