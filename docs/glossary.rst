.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Translation String
     An instance of :class:`repoze.bfg.i18n.TranslationString`, which
     is a class that behaves like a Unicode string, but has several
     extra attributes such as ``domain``, ``msgid``, and ``mapping``
     for use during translation.  Translation strings are usually
     created by hand within software, but are sometimes created on the
     behalf of the system for automatic template translation.  For
     more information, see :ref:`i18n_chapter`.

   Translation String Factory
     A factory for generating :term:`translation string` objects which
     predefines a :term:`translation domain`.

   Translation Domain
     A string representing the "context" in which a particular
     translation was made.  For example the word "java" might be
     translated differently if the translation domain is
     "programming-languages" than would be if the translation domain
     was "coffee".  Every :term:`translation string` has an associated
     translation domain.

