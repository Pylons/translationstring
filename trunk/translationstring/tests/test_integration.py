import unittest

class TranslatorIntegrationTests(unittest.TestCase):
    def _makeTranslations(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        localedir = os.path.join(here, 'fixtures', 'locales')
        from babel.support import Translations
        return Translations.load(localedir, locales=['de'])
        
    def test_translator_ugettext_policy(self):
        translations = self._makeTranslations()
        from translationstring import Translator
        from translationstring import ugettext_policy
        from translationstring import TranslationString

        translator = Translator(translations, ugettext_policy)

        tstring = TranslationString(
            'Enter a comma separated list of user names.')
        
        result = translator(tstring)
        self.assertEqual(result, 'Eine kommagetrennte Liste von Benutzernamen.')
        
    def test_translator_dugettext_policy(self):
        translations = self._makeTranslations()
        from translationstring import Translator
        from translationstring import dugettext_policy
        from translationstring import TranslationString

        translator = Translator(translations, dugettext_policy)

        tstring = TranslationString(
            'Enter a comma separated list of user names.')
        
        result = translator(tstring)
        self.assertEqual(result, 'Eine kommagetrennte Liste von Benutzernamen.')
        
    def test_translator_with_interpolation(self):
        translations = self._makeTranslations()
        from translationstring import Translator
        from translationstring import dugettext_policy
        from translationstring import TranslationString

        translator = Translator(translations, dugettext_policy)

        tstring = TranslationString('Visit ${url}', mapping={'url':'url'})
        
        result = translator(tstring)
        self.assertEqual(result, 'Besuchen url')
        
class PluralizerIntegrationTests(unittest.TestCase):
    def _makeTranslations(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        localedir = os.path.join(here, 'fixtures', 'locales')
        from babel.support import Translations
        return Translations.load(localedir, locales=['de'])
        
    def test_pluralizer_ungettext_policy(self):
        translations = self._makeTranslations()
        from translationstring import Pluralizer
        from translationstring import ungettext_policy

        pluralizer = Pluralizer(translations, ungettext_policy)

        result = pluralizer('Unable to find user: ${users}',
                            'Unable to find users: ${users}',
                            1,
                            mapping={'users':'users'})
        self.assertEqual(result,
                         "Benutzer konnte nicht gefunden werden: users")

    def test_pluralizer_dungettext_policy(self):
        translations = self._makeTranslations()
        from translationstring import Pluralizer
        from translationstring import dungettext_policy

        pluralizer = Pluralizer(translations, dungettext_policy)

        result = pluralizer('Unable to find user: ${users}',
                            'Unable to find users: ${users}',
                            1,
                            domain='messages',
                            mapping={'users':'users'})
        self.assertEqual(result,
                         "Benutzer konnte nicht gefunden werden: users")
