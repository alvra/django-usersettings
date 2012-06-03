try:
    from django.utils import unittest
except ImportError:
    try:
        import unittest2 as unittest
    except ImportError:
        import unittest
if not hasattr(unittest, 'expectedFailure'):
    unittest.skipIf = lambda c, m: (lambda f: f) if c else (lambda f: None)
    unittest.expectedFailure = lambda f: f

from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from usersettings import getsetting, getsettings, setsetting, setsettings, register, Setting, PickledSetting
from usersettings.models import UserSetting


class SimpleSettingTest(unittest.TestCase):
    def setUp(self):
        self.settingname = 'test_setting1'

        class SimpleTestSetting(Setting):
            name = self.settingname
            group = ''

        register.register(SimpleTestSetting())

    def test(self):
        user = User(pk=1)

        self.assertRaises(
            UserSetting.DoesNotExist,
            UserSetting.objects.get,
            user=user,
            name='simple',
        )

        self.assertEqual(getsetting(user, self.settingname), None)
        self.assertEqual(getsettings(user)[self.settingname], None)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: None})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        setsetting(user, self.settingname, 'testvalue')
        self.assertEqual(getsettings(user)[self.settingname], 'testvalue')
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: 'testvalue'})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        self.assertEqual(UserSetting.objects.get(
            user=user,
            name=self.settingname,
        ).value, 'testvalue')

        setsetting(user, self.settingname, None)
        self.assertEqual(getsetting(user, self.settingname), None)
        self.assertEqual(getsettings(user)[self.settingname], None)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: None})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        setsettings(user, {self.settingname: 'testvalue2'})
        self.assertEqual(getsettings(user)[self.settingname], 'testvalue2')
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: 'testvalue2'})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        self.assertEqual(UserSetting.objects.get(
            user=user,
            name=self.settingname,
        ).value, 'testvalue2')

        setsetting(user, self.settingname, None)
        self.assertEqual(getsetting(user, self.settingname), None)
        self.assertEqual(getsettings(user)[self.settingname], None)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: None})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        self.assertRaises(
            UserSetting.DoesNotExist,
            UserSetting.objects.get,
            user=user,
            name='simple',
        )


class PickleSettingTest(unittest.TestCase):
    def setUp(self):
        self.settingname = 'test_setting2'

        class PickleTestSetting(PickledSetting):
            name = self.settingname
            group = ''

        register.register(PickleTestSetting())

    def test(self):
        user = User(pk=1)
        value = dict(
            spam='ham',
            xzsf='sdf',
        )

        self.assertRaises(
            UserSetting.DoesNotExist,
            UserSetting.objects.get,
            user=user,
            name='simple',
        )

        self.assertEqual(getsetting(user, self.settingname), None)
        self.assertEqual(getsettings(user)[self.settingname], None)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: None})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        setsetting(user, self.settingname, value)
        self.assertEqual(getsettings(user)[self.settingname], value)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: value})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        setsetting(user, self.settingname, None)
        self.assertEqual(getsetting(user, self.settingname), None)
        self.assertEqual(getsettings(user)[self.settingname], None)
        self.assertEqual(getsettings(user, [self.settingname]), {self.settingname: None})
        self.assertEqual(getsettings(user, ['nonexisting_setting']), {})

        self.assertRaises(
            UserSetting.DoesNotExist,
            UserSetting.objects.get,
            user=user,
            name='simple',
        )
