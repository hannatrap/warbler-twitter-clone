"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    """Test for message model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("test", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_message_model(self):
        """test basic model"""
        msg = Message(text='testing text', user_id=self.uid)

        db.session.add(msg)
        db.session.commit()

        """user should have one message"""

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "testing text")


    def test_message_likes(self):
        msg1 = Message(text='testing text', user_id=self.uid)

        msg2 = Message(text="more testing text", user_id=self.uid)

        u = User.signup("testuser", "testemail@test.com", "password", None)
        uid=0000
        u.id = uid
        db.session.add([msg1, msg2, u])
        db.session.commit()

        u.likes.append(msg1)
        db.session.commit()

        l=Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, msg1.id)


    def test_message_destroy(self):
        destroy_msg = Message(text='testing text', user_id=self.uid)

        u = User.signup("testuser", "testemail@test.com", "password", None)
        uid=0000
        u.id = uid
        db.session.add([destroy_msg, u])
        db.session.commit()

        u.message.delete(destroy_msg)
        db.session.commit()

        self.assertFalse(self.u.messages(destroy_msg))







