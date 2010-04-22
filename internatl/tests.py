import unittest

class TestTranslationString(unittest.TestCase):
    def _makeOne(self, msgid, **kw):
        from internatl import TranslationString
        return TranslationString(msgid, **kw)

    def test_is_unicode_subclass(self):
        inst = self._makeOne('msgid')
        self.failUnless(isinstance(inst, unicode))

    def test_msgid_is_translation_string(self):
        another = self._makeOne('msgid', domain='domain', default='default',
                                mapping={'a':1})
        result = self._makeOne(another)
        self.assertEqual(result, 'msgid')
        self.assertEqual(result.domain, 'domain')
        self.assertEqual(result.default, 'default')
        self.assertEqual(result.mapping, {'a':1})

    def test_default_None(self):
        inst = self._makeOne('msgid')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.default, 'msgid')

    def test_default_not_None(self):
        inst = self._makeOne('msgid', default='default')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.default, 'default')

    def test_allargs(self):
        inst = self._makeOne('msgid', domain='domain', default='default',
                             mapping='mapping')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.default, 'default')
        self.assertEqual(inst.mapping, 'mapping')
        self.assertEqual(inst.domain, 'domain')

    def test_interpolate_substitution(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne('This is $name version ${version}.',
                              mapping=mapping)
        result = inst.interpolate()
        self.assertEqual(result, u'This is Zope version 3.')

    def test_interpolate_subsitution_more_than_once(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(
            u"This is $name version ${version}. ${name} $version!",
            mapping=mapping)
        result = inst.interpolate()
        self.assertEqual(result, u'This is Zope version 3. Zope 3!')

    def test_interpolate_double_dollar_escape(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne('$$name', mapping=mapping)
        result = inst.interpolate()
        self.assertEqual(result, u'$$name')

    def test_interpolate_missing_not_interpolated(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(
            u"This is $name $version. $unknown $$name $${version}.",
            mapping=mapping)
        result = inst.interpolate()
        self.assertEqual(result,
                         u'This is Zope 3. $unknown $$name $${version}.')

    def test_interpolate_missing_mapping(self):
        inst = self._makeOne(u"This is ${name}")
        result = inst.interpolate()
        self.assertEqual(result, u'This is ${name}')

    def test_interpolate_passed_translated(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(u"This is ${name}", mapping = mapping)
        result = inst.interpolate('That is ${name}')
        self.assertEqual(result, u'That is Zope')

    def test_ugettext_translations_None_interpolation_required(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(u"This is ${name}", mapping = mapping)
        result = inst.ugettext()
        self.assertEqual(result, u'This is Zope')
        
    def test_ugettext_translations_None_interpolation_not_required(self):
        inst = self._makeOne(u"This is ${name}")
        result = inst.ugettext()
        self.assertEqual(result, u'This is ${name}')

    def test_ugettext_translations_returns_msgid(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(u"This is ${name}", default='another ${name}',
                             mapping=mapping)
        class Translations(object):
            def ugettext(self, msg):
                return msg
        translations = Translations()
        result = inst.ugettext(translations)
        self.assertEqual(result, 'another Zope')

    def test_ugettext_translations_returns_translation(self):
        mapping = {"name": "Zope", "version": 3}
        inst = self._makeOne(u"This is ${name}", default='another ${name}',
                             mapping=mapping)
        class Translations(object):
            def ugettext(self, msg):
                return 'Woo hoo ${name}'
        translations = Translations()
        result = inst.ugettext(translations)
        self.assertEqual(result, 'Woo hoo Zope')

class TestTranslationStringFactory(unittest.TestCase):
    def _makeOne(self, domain):
        from internatl import TranslationStringFactory
        return TranslationStringFactory(domain)

    def test_allargs(self):
        factory = self._makeOne('budge')
        inst = factory('msgid', mapping='mapping', default='default')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.domain, 'budge')
        self.assertEqual(inst.mapping, 'mapping')
        self.assertEqual(inst.default, 'default')


class TestChameleonTranslate(unittest.TestCase):
    def _makeOne(self, translator):
        from internatl import ChameleonTranslate
        return ChameleonTranslate(translator)

    def test_msgid_nonstring(self):
        translate = self._makeOne(None)
        result = translate(None)
        self.assertEqual(result, None)

    def test_msgid_translationstring_translator_is_None(self):
        msgid = DummyTranslationString()
        translate = self._makeOne(None)
        result = translate(msgid)
        self.assertEqual(result, 'interpolated')

    def test_msgid_unicode_translator_is_None(self):
        msgid = u'foo'
        translate = self._makeOne(None)
        result = translate(msgid)
        self.assertEqual(result, u'foo')

    def test_msgid_translationstring_translator_is_not_None(self):
        msgid = DummyTranslationString()
        def translator(msg):
            return msg
        translate = self._makeOne(translator)
        result = translate(msgid)
        self.assertEqual(result, msgid)

    def test_msgid_unicode_translator_is_not_None(self):
        msgid = 'foo'
        def translator(msg):
            return msg
        translate = self._makeOne(translator)
        result = translate(msgid)
        self.assertEqual(result, msgid)

class TestTranslator(unittest.TestCase):
    def _makeOne(self, translations):
        from internatl import Translator
        return Translator(translations)

    def test_it(self):
        translations = 'abc'
        translator = self._makeOne(translations)
        tstring = DummyTranslationString()
        result = translator(tstring)
        self.assertEqual(result, 'ugottext')

class DummyTranslationString(unicode):
    def ugettext(self, translations):
        self.translations = translations
        return 'ugottext'
    
    def interpolate(self):
        return 'interpolated'
    
