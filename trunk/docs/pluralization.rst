Pluralization
=============

:func:`translationstring.Pluralizer` provides a gettext "plural forms"
pluralization service.

It is called like so:

.. code-block:: python
   :linenos:

   import gettext
   from translationstring import Pluralizer
   translations = gettext.translations(.. the right arguments ...)
   pluralizer = Pluralizer(translations)

The ``translations`` argument is required; it should be an object
supporting *at least* the Python :class:`gettext.NullTranslations` API
but ideally the :class:`babel.support.Translations` API, which has
support for domain lookups like dungettext.

The object returned will be a callable which has the following
signature:

.. code-block:: python
   :linenos:

   def pluralizer(singular, plural, n, domain=None, mapping=None):
       """ Pluralize """

The ``singular`` and ``plural`` arguments passed may be translation
strings or unicode strings.  ``n`` represents the number of elements.
``domain`` is the translation domain to use to do the pluralization,
and ``mapping`` is the interpolation mapping that should be used on
the result.  The pluralizer will return the plural form or the
singular form, translated, as necessary.

.. note:: 

  if the objects passed are translation strings, their domains and
  mappings are ignored.  The domain and mapping arguments must be used
  instead.  If the ``domain`` is not supplied, a default domain is
  used (usually ``messages``).

If ``translations`` is ``None``, a :class:`gettext.NullTranslations`
object is created for the pluralizer to use.

The :func:`translationstring.Pluralizer` function accepts an
additional optional argument named ``policy``.  ``policy`` should be a
callable which accepts five arguments: ``translations``, ``singular``
and ``plural``, ``n`` and ``domain``.  It must perform the actual
pluralization lookup.  If ``policy`` is ``None``, the
:func:`translationstring.dungettext_policy` policy will be used.

