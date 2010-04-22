import unittest

class IntegrationTests(unittest.TestCase):
    def test_translator_ugettext_policy(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        localedir = os.path.join(here, 'fixtures', 'locales')
        from gettext import translation
        from internatl import Translator
        from internatl import ugettext_policy
        from internatl import TranslationString

        translations = translation('messages', localedir, languages=['de'])
        translator = Translator(translations, ugettext_policy)

        tstring = TranslationString(
            'Enter a comma separated list of user names.')
        
        result = translator(tstring)
        self.assertEqual(result, 'Eine kommagetrennte Liste von Benutzernamen.')
        
    def test_translator_dugettext_policy(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        localedir = os.path.join(here, 'fixtures', 'locales')
        from babel.support import Translations
        from internatl import Translator
        from internatl import dugettext_policy
        from internatl import TranslationString

        translations = Translations.load(localedir, locales=['de'])
        translator = Translator(translations, dugettext_policy)

        tstring = TranslationString(
            'Enter a comma separated list of user names.')
        
        result = translator(tstring)
        self.assertEqual(result, 'Eine kommagetrennte Liste von Benutzernamen.')
        
    def test_translator_with_interpolation(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        localedir = os.path.join(here, 'fixtures', 'locales')
        from babel.support import Translations
        from internatl import Translator
        from internatl import dugettext_policy
        from internatl import TranslationString

        translations = Translations.load(localedir, locales=['de'])
        translator = Translator(translations, dugettext_policy)

        tstring = TranslationString('Visit ${url}', mapping={'url':'url'})
        
        result = translator(tstring)
        self.assertEqual(result, 'Besuchen url')
        
