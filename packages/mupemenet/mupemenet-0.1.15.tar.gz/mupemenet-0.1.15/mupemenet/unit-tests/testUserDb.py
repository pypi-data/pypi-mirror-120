import unittest

from mupemenet.userdb.UserDB import UserDB


class TestUserDb(unittest.TestCase):

    def test_upsert_timestamp(self):
        db = UserDB()
        dummy_timestamp = 1234567890
        db.set_latest_timestamp(dummy_timestamp)
        retrieved_dummy_timestamp = db.get_latest_timestamp()
        self.assertTrue(dummy_timestamp == retrieved_dummy_timestamp)

    def test_count_users(self):
        n = UserDB().count_users()
        print("Number of users: {}".format(n))
        self.assertGreater(n, 3)

    def test_build_fr_model(self):
        ret_val = UserDB().build_fr_model()
        self.assertTrue(ret_val)
