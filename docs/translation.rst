.. _translation_chapter:

Translation
===========

:mod:`translationstring` provides a function named
:func:`translationstring.Translator` which is used to create a
:term:`translator` object.

It is called like so:

.. code-block:: python
   :linenos:

   import gettext
   from translationstring import Translator
   translations = gettext.translations(.. the right arguments ...)
   translator = Translator(translations)

The ``translations`` argument is required; it should be an object
supporting *at least* the Python :class:`gettext.NullTranslations` API
but ideally the :class:`babel.support.Translations` API, which has
support for domain lookups like dugettext.

The callable returned accepts three arguments: a translation string
``tstring`` (required), ``domain`` (optional), and ``mapping``
(optional).  When called, it will translate the ``tstring``
translation string to a ``unicode`` object using the ``translations``
object provided and interpolate the result.

.. code-block:: python
   :linenos:

   from gettext import translations
   from translationstring import Translator
   from translationstring import TranslationString

   t = translations(.. the right arguments ...)
   translator = Translator(t)
   ts = TranslationString('Add ${number}', domain='foo', mapping={'number':1})
   translator(ts)

If ``translations`` is ``None``, the result of interpolation of the
msgid or default value of the translation string is returned.

The translation function can also deal with plain Unicode objects.
The optional ``domain`` argument can be used to specify or override
the domain of the ``tstring`` argument (useful when ``tstring`` is a
normal string rather than a translation string).  The optional
``mapping`` argument can specify the interpolation mapping, useful
when the ``tstring`` argument is not a translation string. If 
``tstring`` is a translation string its mapping data, if present, is
combined with the data from the ``mapping`` argument.

.. code-block:: python
   :linenos:

   from gettext import translations
   from translationstring import Translator
   from translationstring import TranslationString

   t = translations(.. the right arguments ...)
   translator = Translator(t)
   translator('Add ${number}', domain='foo', mapping={'number':1})

The :func:`translationstring.Translator` function accepts an
additional optional argument named ``policy``.  ``policy`` should be a
callable which accepts three arguments: ``translations``, ``tstring``
and ``domain``.  It must perform the actual translation lookup.  If
``policy`` is ``None``, the :func:`translationstring.dugettext_policy`
policy will be used.

