import gettext
from six import PY3

if PY3:
    gettext.GNUTranslations.ugettext = gettext.GNUTranslations.gettext
    gettext.GNUTranslations.ungettext = gettext.GNUTranslations.ngettext
    
#
# Brought in from Babel during the effort to port translationstring to Python 3,
# in order to avoid porting all of Babel.
#
class Translations(gettext.GNUTranslations, object):
    """An extended translation catalog class."""

    DEFAULT_DOMAIN = 'messages'

    def __init__(self, fileobj=None, domain=DEFAULT_DOMAIN):
        """Initialize the translations catalog.

        :param fileobj: the file-like object the translation should be read
                        from
        """
        gettext.GNUTranslations.__init__(self, fp=fileobj)
        self.files = filter(None, [getattr(fileobj, 'name', None)])
        self.domain = domain
        self._domains = {}

    def load(cls, dirname=None, locales=None, domain=DEFAULT_DOMAIN):
        """Load translations from the given directory.

        :param dirname: the directory containing the ``MO`` files
        :param locales: the list of locales in order of preference (items in
                        this list can be either `Locale` objects or locale
                        strings)
        :param domain: the message domain
        :return: the loaded catalog, or a ``NullTranslations`` instance if no
                 matching translations were found
        :rtype: `Translations`
        """
        if locales is not None:
            if not isinstance(locales, (list, tuple)):
                locales = [locales]
            locales = [str(locale) for locale in locales]
        if not domain:
            domain = cls.DEFAULT_DOMAIN
        filename = gettext.find(domain, dirname, locales)
        if not filename:
            return gettext.NullTranslations()
        return cls(fileobj=open(filename, 'rb'), domain=domain)
    load = classmethod(load)

    def __repr__(self):
        return '<%s: "%s">' % (type(self).__name__,
                               self._info.get('project-id-version'))

    def add(self, translations, merge=True):
        """Add the given translations to the catalog.

        If the domain of the translations is different than that of the
        current catalog, they are added as a catalog that is only accessible
        by the various ``d*gettext`` functions.

        :param translations: the `Translations` instance with the messages to
                             add
        :param merge: whether translations for message domains that have
                      already been added should be merged with the existing
                      translations
        :return: the `Translations` instance (``self``) so that `merge` calls
                 can be easily chained
        :rtype: `Translations`
        """
        domain = getattr(translations, 'domain', self.DEFAULT_DOMAIN)
        if merge and domain == self.domain:
            return self.merge(translations)

        existing = self._domains.get(domain)
        if merge and existing is not None:
            existing.merge(translations)
        else:
            translations.add_fallback(self)
            self._domains[domain] = translations

        return self

    def merge(self, translations):
        """Merge the given translations into the catalog.

        Message translations in the specified catalog override any messages
        with the same identifier in the existing catalog.

        :param translations: the `Translations` instance with the messages to
                             merge
        :return: the `Translations` instance (``self``) so that `merge` calls
                 can be easily chained
        :rtype: `Translations`
        """
        if isinstance(translations, gettext.GNUTranslations):
            self._catalog.update(translations._catalog)
            if isinstance(translations, Translations):
                self.files.extend(translations.files)

        return self

    def dgettext(self, domain, message):
        """Like ``gettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).gettext(message)
    
    def ldgettext(self, domain, message):
        """Like ``lgettext()``, but look the message up in the specified 
        domain.
        """ 
        return self._domains.get(domain, self).lgettext(message)
    
    def dugettext(self, domain, message):
        """Like ``ugettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).ugettext(message)
    
    def dngettext(self, domain, singular, plural, num):
        """Like ``ngettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).ngettext(singular, plural, num)
    
    def ldngettext(self, domain, singular, plural, num):
        """Like ``lngettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).lngettext(singular, plural, num)
    
    def dungettext(self, domain, singular, plural, num):
        """Like ``ungettext()`` but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).ungettext(singular, plural, num)

    # Most of the downwards code, until it get's included in stdlib, from:
    #    http://bugs.python.org/file10036/gettext-pgettext.patch
    #    
    # The encoding of a msgctxt and a msgid in a .mo file is
    # msgctxt + "\x04" + msgid (gettext version >= 0.15)
    CONTEXT_ENCODING = '%s\x04%s'

    def pgettext(self, context, message):
        """Look up the `context` and `message` id in the catalog and return the
        corresponding message string, as an 8-bit string encoded with the
        catalog's charset encoding, if known.  If there is no entry in the
        catalog for the `message` id and `context` , and a fallback has been
        set, the look up is forwarded to the fallback's ``pgettext()``
        method. Otherwise, the `message` id is returned.
        """
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.pgettext(context, message)
            return message
        # Encode the Unicode tmsg back to an 8-bit string, if possible
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        elif self._charset:
            return tmsg.encode(self._charset)
        return tmsg

    def lpgettext(self, context, message):
        """Equivalent to ``pgettext()``, but the translation is returned in the
        preferred system encoding, if no other encoding was explicitly set with
        ``bind_textdomain_codeset()``.
        """
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.lpgettext(context, message)
            return message
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        return tmsg.encode(locale.getpreferredencoding())

    def npgettext(self, context, singular, plural, num):
        """Do a plural-forms lookup of a message id.  `singular` is used as the
        message id for purposes of lookup in the catalog, while `num` is used to
        determine which plural form to use.  The returned message string is an
        8-bit string encoded with the catalog's charset encoding, if known.
        
        If the message id for `context` is not found in the catalog, and a
        fallback is specified, the request is forwarded to the fallback's
        ``npgettext()`` method.  Otherwise, when ``num`` is 1 ``singular`` is
        returned, and ``plural`` is returned in all other cases.
        """
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, singular)
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(num))]
            if self._output_charset:
                return tmsg.encode(self._output_charset)
            elif self._charset:
                return tmsg.encode(self._charset)
            return tmsg
        except KeyError:
            if self._fallback:
                return self._fallback.npgettext(context, singular, plural, num)
            if num == 1:
                return singular
            else:
                return plural

    def lnpgettext(self, context, singular, plural, num):
        """Equivalent to ``npgettext()``, but the translation is returned in the
        preferred system encoding, if no other encoding was explicitly set with
        ``bind_textdomain_codeset()``.
        """
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, singular)
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(num))]
            if self._output_charset:
                return tmsg.encode(self._output_charset)
            return tmsg.encode(locale.getpreferredencoding())
        except KeyError:
            if self._fallback:
                return self._fallback.lnpgettext(context, singular, plural, num)
            if num == 1:
                return singular
            else:
                return plural

    def upgettext(self, context, message):
        """Look up the `context` and `message` id in the catalog and return the
        corresponding message string, as a Unicode string.  If there is no entry
        in the catalog for the `message` id and `context`, and a fallback has
        been set, the look up is forwarded to the fallback's ``upgettext()``
        method.  Otherwise, the `message` id is returned.
        """
        ctxt_message_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_message_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.upgettext(context, message)
            return unicode(message)
        return tmsg

    def unpgettext(self, context, singular, plural, num):
        """Do a plural-forms lookup of a message id.  `singular` is used as the
        message id for purposes of lookup in the catalog, while `num` is used to
        determine which plural form to use.  The returned message string is a
        Unicode string.
        
        If the message id for `context` is not found in the catalog, and a
        fallback is specified, the request is forwarded to the fallback's
        ``unpgettext()`` method.  Otherwise, when `num` is 1 `singular` is
        returned, and `plural` is returned in all other cases.
        """
        ctxt_message_id = self.CONTEXT_ENCODING % (context, singular)
        try:
            tmsg = self._catalog[(ctxt_message_id, self.plural(num))]
        except KeyError:
            if self._fallback:
                return self._fallback.unpgettext(context, singular, plural, num)
            if num == 1:
                tmsg = unicode(singular)
            else:
                tmsg = unicode(plural)
        return tmsg

    def dpgettext(self, domain, context, message):
        """Like `pgettext()`, but look the message up in the specified
        `domain`.
        """
        return self._domains.get(domain, self).pgettext(context, message)
    
    def dupgettext(self, domain, context, message):
        """Like `upgettext()`, but look the message up in the specified
        `domain`.
        """
        return self._domains.get(domain, self).upgettext(context, message)

    def ldpgettext(self, domain, context, message):
        """Equivalent to ``dpgettext()``, but the translation is returned in the
        preferred system encoding, if no other encoding was explicitly set with
        ``bind_textdomain_codeset()``.
        """
        return self._domains.get(domain, self).lpgettext(context, message)

    def dnpgettext(self, domain, context, singular, plural, num):
        """Like ``npgettext``, but look the message up in the specified
        `domain`.
        """
        return self._domains.get(domain, self).npgettext(context, singular,
                                                         plural, num)
        
    def dunpgettext(self, domain, context, singular, plural, num):
        """Like ``unpgettext``, but look the message up in the specified
        `domain`.
        """
        return self._domains.get(domain, self).unpgettext(context, singular,
                                                          plural, num)

    def ldnpgettext(self, domain, context, singular, plural, num):
        """Equivalent to ``dnpgettext()``, but the translation is returned in
        the preferred system encoding, if no other encoding was explicitly set
        with ``bind_textdomain_codeset()``.
        """
        return self._domains.get(domain, self).lnpgettext(context, singular,
                                                          plural, num)