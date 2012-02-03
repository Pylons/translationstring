.. _tstrings_chapter:

Translation Strings
===================

While you write your software, you can insert specialized markup into
your Python code that makes it possible for the system to translate
text values into the languages used by your application's users.  This
markup generates a :term:`translation string`.  A translation string
is an object that behave mostly like a normal Unicode object, except
that it also carries around extra information related to its job as
part of a higher-level system's translation machinery.

.. note:: Using a translation string can be thought of as equivalent
   to using a "lazy string" object in other i18n systems.

Using The ``TranslationString`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most primitive way to create a translation string is to use the
:class:`translationstring.TranslationString` callable:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add')

This creates a Unicode-like object that is a
:class:`translationstring.TranslationString`.

.. note::

   For people familiar with Zope internationalization, a
   TranslationString is a lot like a ``zope.i18nmessageid.Message``
   object.  It is not a subclass, however.

The first argument to :class:`translationstring.TranslationString` is the
``msgid``; it is required.  It represents the key into the translation
mappings provided by a particular localization. The ``msgid`` argument
must be a Unicode object or an ASCII string.  The msgid may optionally
contain *replacement markers*.  For instance:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add ${number}')

Within the string above, ``${stuff}`` is a replacement marker.  It
will be replaced by whatever is in the *mapping* for a translation
string when the :meth:`translationstring.TranslationString.interpolate` method
is called.  The mapping may be supplied at the same time as the
replacement marker itself:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add ${number}', mapping={'number':1})

You can also create a new translation string instance with a mapping
using the standard python %-operator:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add ${number}') % {'number': 1}

You may interpolate a translation string with a mapping:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add ${number}', mapping={'number':1})
   result = ts.interpolate()

The above ``result`` will be ``Add 1``.

Any number of replacement markers can be present in the msgid value,
any number of times.  Only markers which can be replaced by the values
in the *mapping* will be replaced at translation time.  The others
will not be interpolated and will be output literally.

Replacement markers may also be spelled without squiggly braces:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add $number', mapping={'number':1})

The ``Add $number`` msgid above is equivalent to ``Add ${number}``.

A translation string should also usually carry a *domain*.  The domain
represents a translation category to disambiguate it from other
translations of the same msgid, in case they conflict.

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('Add ${number}', mapping={'number':1}, 
                          domain='form')

The above translation string named a domain of ``form``.  A
*translator* function (see :ref:`translation_chapter`) will often use
the domain to locate the right translator file on the filesystem which
contains translations for a given domain.  In this case, if it were
trying to translate to our msgid to German, it might try to find a
translation from a :term:`gettext` file within a :term:`translation
directory` like this one::

   locale/de/LC_MESSAGES/form.mo

In other words, it would want to take translations from the ``form.mo``
translation file in the German language.

Finally, the TranslationString constructor accepts a ``default``
argument.  If a ``default`` argument is supplied, it replaces usages
of the ``msgid`` as the *default value* for the translation string.
When ``default`` is ``None``, the ``msgid`` value passed to a
TranslationString is used as an implicit message identifier.  Message
identifiers are matched with translations in translation files, so it
is often useful to create translation strings with "opaque" message
identifiers unrelated to their default text:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString
   ts = TranslationString('add-number', default='Add ${number}',
                           domain='form', mapping={'number':1})

When a ``default`` value is used, the default may contain replacement
markers and the msgid should not contain replacement markers.

Using the ``TranslationStringFactory`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another way to generate a translation string is to use the
:attr:`translationstring.TranslationStringFactory` object.  This object is a
*translation string factory*.  Basically a translation string factory
presets the ``domain`` value of any :term:`translation string`
generated by using it.  For example:

.. code-block:: python
   :linenos:

   from translationstring import TranslationStringFactory
   _ = TranslationStringFactory('bfg')
   ts = _('add-number', default='Add ${number}', mapping={'number':1})

.. note:: We assigned the translation string factory to the name
   ``_``.  This is a convention which will be supported by translation
   file generation tools.

After assigning ``_`` to the result of a
:func:`translationstring.TranslationStringFactory`, the subsequent
result of calling ``_`` will be a
:class:`translationstring.TranslationString` instance.  Even though a
``domain`` value was not passed to ``_`` (as would have been necessary
if the :class:`translationstring.TranslationString` constructor were
used instead of a translation string factory), the ``domain``
attribute of the resulting translation string will be ``bfg``.  As a
result, the previous code example is completely equivalent (except for
spelling) to:

.. code-block:: python
   :linenos:

   from translationstring import TranslationString as _
   ts = _('add-number', default='Add ${number}', mapping={'number':1}, 
          domain='bfg')

You can set up your own translation string factory much like the one
provided above by using the
:class:`translationstring.TranslationStringFactory` class.  For example,
if you'd like to create a translation string factory which presets the
``domain`` value of generated translation strings to ``form``, you'd
do something like this:

.. code-block:: python
   :linenos:

   from translationstring import TranslationStringFactory
   _ = TranslationStringFactory('form')
   ts = _('add-number', default='Add ${number}', mapping={'number':1})

.. note::

   For people familiar with Zope internationalization, a
   TranslationStringFactory is a lot like a
   ``zope.i18nmessageid.MessageFactoy`` object.  It is not a subclass,
   however.

Pickleability
-------------

Translation strings may be pickled and unpickled.
