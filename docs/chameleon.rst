Chameleon Translate Function Support
=====================================

:func:`translationstring.ChameleonTranslate` is a function which
returns a callable suitable for use as the ``translate`` argument to
various ``PageTemplate*`` constructors.

.. code-block:: python
   :linenos:

   from chameleon.zpt.template import PageTemplate
   from translationstring import ChameleonTranslate
   from translationstring import Translator
   import gettext

   translations = gettext.translations(...)
   translator = Translator(translations)
   translate = ChameleonTranslate(translate)
   pt = PageTemplate('<html></html>', translate=translate)

The ``translator`` provided should be a callable which accepts a
single argument ``translation_string`` ( a
:class:`translationstring.TranslationString` instance) which returns a
``unicode`` object as a translation; usually the result of calling
:func:`translationstring.Translator`.  ``translator`` may also
optionally be ``None``, in which case no translation is performed (the
``msgid`` or ``default`` value is returned untranslated).
