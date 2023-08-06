from unittest.case import skip
from mupemenet.services.Jobs import install, package_exist, uninstall
import unittest
from mupemenet.config.Config import Config
from mupemenet.userdb.UserDB import UserDB


class TestUserDb(unittest.TestCase):

    @unittest.skip
    def test_upsert_timestamp(self):
        db = UserDB()
        dummy_timestamp = 1234567890
        db.set_latest_timestamp(dummy_timestamp)
        retrieved_dummy_timestamp = db.get_latest_timestamp()
        self.assertTrue(dummy_timestamp == retrieved_dummy_timestamp)

    @unittest.skip
    def test_count_users(self):
        n = UserDB().count_users()
        print("Number of users: {}".format(n))
        self.assertGreater(n, 3)

    @unittest.skip
    def test_build_fr_model(self):
        ret_val = UserDB().build_fr_model()
        self.assertTrue(ret_val)

    def test_env_path(self):
        Config(env='release')
        self.assertTrue('release' in Config.ENV)

    def test_package_existens(self):
        self.assertTrue(package_exist('schedule'))
        self.assertFalse(package_exist('random_package_that_does_not_exist'))

    @unittest.skip
    def test_install_random_package(self):
        package = 'panglery'
        self.assertFalse(package_exist(package))
        install(package)
        self.assertTrue(package_exist(package))







if __name__ == '__main__':
    unittest.main()
