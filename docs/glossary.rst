.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Translation String
     An instance of :class:`translationstring.TranslationString`,
     which is a class that behaves like a Unicode string, but has
     several extra attributes such as ``domain``, ``msgid``, and
     ``mapping`` for use during translation.  Translation strings are
     usually created by hand within software, but are sometimes
     created on the behalf of the system for automatic template
     translation.  For more information, see
     :ref:`translationstring_module`.

   Translation String Factory
     A factory for generating :term:`translation string` objects which
     predefines a :term:`translation domain`.

   Translation Domain
     A string representing the "domain" in which a particular
     translation was made.  Normally represents the project / package name
     that defines the term.  Every :term:`translation string` has an
     associated translation domain.

   Translation Context
     An optional string added to help resolve translation ambiguities
     associated with very short terms, such as those which appear in
     GUI menus, etc.  See:
     https://www.gnu.org/software/gettext/manual/gettext.html#Contexts

   Message Identifier
     An unchanging string that is the identifier for a particular
     translation string.  For example, you may have a translation
     string which has the ``default`` "the fox jumps over the lazy
     dog", but you might give this translation string a message
     identifier of ``foxdog`` to reduce the chances of minor spelling
     or wording changes breaking your translations.  The message
     identifier of a :term:`translation string` is represented as its
     ``msgid`` argument.

   Translation Directory
     A translation directory is a :term:`gettext` translation
     directory.  It contains language folders, which themselves
     contain ``LC_MESSAGES`` folders, which contain ``.mo`` files.
     Each ``.mo`` file represents a set of translations for a language
     in a :term:`translation domain`.  The name of the ``.mo`` file
     (minus the .mo extension) is the translation domain name.

   Gettext
     The GNU `gettext <http://www.gnu.org/software/gettext/>`_
     library, used by the :mod:`translationstring` locale translation
     machinery.

   Translator
     A callable which receives a :term:`translation string` and
     returns a translated Unicode object for the purposes of
     internationalization.  

   Babel
     A `collection of tools <http://babel.pocoo.org/en/latest/>`_ for
     internationalizing Python applications.

   Chameleon
     `chameleon <https://chameleon.readthedocs.io/en/latest/>`_ is templating
     language written and maintained by Malthe Borch.
