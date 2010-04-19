import unittest

class TestTranslationString(unittest.TestCase):
    def _makeOne(self, text, **kw):
        from internatl import TranslationString
        return TranslationString(text, **kw)

    def test_msgid_None(self):
        inst = self._makeOne('text')
        self.assertEqual(inst, 'text')
        self.assertEqual(inst.default, 'text')

    def test_msgid_not_None(self):
        inst = self._makeOne('text', msgid='msgid')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.default, 'text')

    def test_allargs(self):
        inst = self._makeOne('text', msgid='msgid', mapping='mapping',
                             domain='domain')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.default, 'text')
        self.assertEqual(inst.mapping, 'mapping')
        self.assertEqual(inst.domain, 'domain')

class TestTranslationStringFactory(unittest.TestCase):
    def _makeOne(self, domain):
        from internatl import TranslationStringFactory
        return TranslationStringFactory(domain)

    def test_allargs(self):
        factory = self._makeOne('budge')
        inst = factory('text', mapping='mapping', msgid='msgid')
        self.assertEqual(inst, 'msgid')
        self.assertEqual(inst.domain, 'budge')
        self.assertEqual(inst.mapping, 'mapping')
        self.assertEqual(inst.default, 'text')


class TestChameleonTranslate(unittest.TestCase):
    def _makeOne(self, translator):
        from internatl import ChameleonTranslate
        return ChameleonTranslate(translator)

    def test_text_None(self):
        trans = self._makeOne(None)
        result = trans(None)
        self.assertEqual(result, None)

    def test_text_is_nonstring(self):
        def translator(text):
            return text
        trans = self._makeOne(translator)
        result = trans('text')
        self.assertEqual(result, 'text')
        self.assertEqual(result.domain, None)
        self.assertEqual(result.default, 'text')
        self.assertEqual(result.mapping, {})

    def test_with_allargs(self):
        def translator(text):
            return text
        trans = self._makeOne(translator)
        result = trans('text', domain='domain', mapping={'a':'1'},
                       context=None, target_language='lang',
                       default='default')
        self.assertEqual(result, 'text')
        self.assertEqual(result.domain, 'domain')
        self.assertEqual(result.default, 'default')
        self.assertEqual(result.mapping, {'a':'1'})

class Test_interpolate(unittest.TestCase):
    def _callFUT(self, text, mapping=None):
        from internatl import interpolate
        return interpolate(text, mapping)

    def test_substitution(self):
        mapping = {"name": "Zope", "version": 3}
        result = self._callFUT(u"This is $name version ${version}.", mapping)
        self.assertEqual(result, u'This is Zope version 3.')

    def test_subsitution_more_than_once(self):
        mapping = {"name": "Zope", "version": 3}
        result = self._callFUT(
            u"This is $name version ${version}. ${name} $version!",
            mapping)
        self.assertEqual(result, u'This is Zope version 3. Zope 3!')

    def test_double_dollar_escape(self):
        mapping = {"name": "Zope", "version": 3}
        result = self._callFUT('$$name', mapping)
        self.assertEqual(result, u'$$name')

    def test_missing_not_interpolated(self):
        mapping = {"name": "Zope", "version": 3}
        result = self._callFUT(
            u"This is $name $version. $unknown $$name $${version}.",
            mapping)
        self.assertEqual(result,
                         u'This is Zope 3. $unknown $$name $${version}.')

    def test_missing_mapping(self):
        result = self._callFUT(u"This is ${name}")
        self.assertEqual(result, u'This is ${name}')

