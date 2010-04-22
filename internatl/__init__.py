import re

NAME_RE = r"[a-zA-Z][-a-zA-Z0-9_]*"

_interp_regex = re.compile(r'(?<!\$)(\$(?:(%(n)s)|{(%(n)s)}))'
    % ({'n': NAME_RE}))

class TranslationString(unicode):
    """
    The constructor for a :term:`translation string`.  A translation
    string is a Unicode-like object that has some extra metadata.

    This constructor accepts one required argument named ``msgid``.
    ``msgid`` must be the :term:`message identifier` for the
    translation string.  It must be a ``unicode`` object or a ``str``
    object encoded in the default system encoding.

    Optional keyword arguments to this object's constructor include
    ``domain``, ``default``, and ``mapping``.

    ``domain`` represents the :term:`translation domain`.  By default,
    the translation domain is ``None``, indicating that this
    translation string is associated with the :term:`default
    translation domain`.

    ``default`` represents an explicit *default text* for this
    translation string.  Default text appears when the translation
    string cannot be translated.  Usually, the ``msgid`` of a
    translation string serves double duty as as its default text.
    However, using this option you can provide a different default
    text for this translation string.  This feature is useful when the
    default of a translation string is too complicated or too long to
    be used as a message identifier. If ``default`` is provided, it
    must be a ``unicode`` object or a ``str`` object encoded in the
    default system encoding (usually means ASCII).  If ``default`` is
    ``None`` (its default value), the ``msgid`` value used by this
    translation string will be assumed to be the value of ``default``.

    ``mapping``, if supplied, must be a dictionary-like object which
    represents the replacement values for any :term:`translation
    replacement marker` instances found within the ``msgid`` (or
    ``default``) value of this translation string.

    After a translation string is constructed, it behaves like most
    other ``unicode`` objects; its ``msgid`` value will be displayed
    when it is treated like a ``unicode`` object.  Only when its
    ``ugettext`` method is called will it be translated.

    Its default value is available as the ``default`` attribute of the
    object, its :term:`translation domain` is available as the
    ``domain`` attribute, and the ``mapping`` is available as the
    ``mapping`` attribute.  The object otherwise behaves much like a
    Unicode string.
    """
    __slots__ = ('domain', 'default', 'mapping')

    def __new__(self, msgid, domain=None, default=None, mapping=None):
        self = unicode.__new__(self, msgid)
        if isinstance(msgid, self.__class__):
            domain = msgid.domain and msgid.domain[:] or domain
            default = msgid.default and msgid.default[:] or default
            mapping = msgid.mapping and msgid.mapping.copy() or mapping
            msgid = unicode(msgid)
        self.domain = domain
        if default is None:
            default = msgid
        self.default = unicode(default)
        self.mapping = mapping
        return self

    def interpolate(self, translated=None):
        """ Interpolate the value ``translated`` which is assumed to
        be a Unicode object containing zero or more *replacement
        markers* (``${foo}`` or ``${bar}``) using the ``mapping``
        dictionary attached to this instance.  If the ``mapping``
        dictionary is empty or ``None``, no interpolation is
        performed.

        If ``translated`` is ``None``, interpolation will be performed
        against the ``default`` value.
        """
        if translated is None:
            translated = self.default
        if self.mapping and translated:
            def replace(match):
                whole, param1, param2 = match.groups()
                return unicode(self.mapping.get(param1 or param2, whole))
            translated = _interp_regex.sub(replace, translated)

        return translated

    def ugettext(self, translations=None):
        """ Translate this translation string to a ``unicode`` object
        using the ``translations`` provided.  The ``translations``
        provided should be an object supporting the Python
        :class:`gettext.NullTranslations` API.  If ``translations`` is
        None, the result of interpolation of the default value is
        returned."""
        translated = self
        if translations is not None:
            translated = translations.ugettext(translated)
        if translated == self:
            translated = self.default
        if self.mapping and translated:
            translated = self.interpolate(translated)
        return translated

def TranslationStringFactory(domain):
    """ Create a factory which will generate translation strings
    without requiring that each call to the factory be passed a
    ``domain`` value.  A single argument is passed to this class'
    constructor: ``domain``.  This value will be used as the
    ``domain`` values of :class:`internatl.TranslationString` objects
    generated by the ``__call__`` of this class.  The ``msgid``,
    ``mapping``, and ``default`` values provided to the ``__call__``
    method of an instance of this class have the meaning as described
    by the constructor of the :class:`internatl.TranslationString`"""
    def create(msgid, mapping=None, default=None):
        """ Provided a msgid (Unicode object or :term:`translation
        string`) and optionally a mapping object, and a *default
        value*, return a :term:`translation string` object."""
        return TranslationString(msgid, domain=domain, default=default,
                                 mapping=mapping)
    return create

def ChameleonTranslate(translator):
    """
    When necessary, use the result of calling this function as a
    Chameleon template 'translate' function (e.g. the ``translate``
    argument to the ``chameleon.zpt.template.PageTemplate``
    constructor) to allow our translation machinery to drive template
    translation.  A single required argument ``translator`` is
    passsed.  The ``translator`` provided should be a callable which
    accepts a single argument ``translation_string`` ( a
    :class:`internatl.TranslationString` instance) which returns a
    ``unicode`` object as a translation.  ``translator`` may also
    optionally be ``None``, in which case no translation is performed
    (the ``msgid`` or ``default`` value is returned untranslated).
    """
    def translate(msgid, domain=None, mapping=None, context=None,
                 target_language=None, default=None):
        if not isinstance(msgid, basestring):
            return msgid

        tstring = msgid

        if not hasattr(tstring, 'ugettext'):
            tstring = TranslationString(msgid, domain, default, mapping)

        if translator is None:
            result = tstring.interpolate()
        else:
            result = translator(tstring)

        return result

    return translate

def Translator(translations):
    def translator(tstring):
        return tstring.ugettext(translations)
    return translator


