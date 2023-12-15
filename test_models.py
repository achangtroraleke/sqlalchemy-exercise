from unittest import TestCase

from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.app_context().push()

class UserModelTestCase(TestCase):


    def setUp(self):
        print('HELLO')
        db.create_all()
        test_user = User(first_name = 'test', last_name = 'tester', image_url='image')
        db.session.add(test_user)
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

    def test_create_user(self):
        test_user = User(first_name = 'test', last_name = 'tester', image_url='image')
        db.session.add(test_user)
        db.session.commit()
        tester = User.query.filter_by(first_name='test').first()
        self.assertEqual(tester.first_name, 'test')

    def test_delete_user(self):
        tester = User.query.filter_by(first_name='test').first()
        db.session.delete(tester)
        db.session.commit()
        table = User.query.all()
        self.assertEqual(len(table), 0)

    def test_update_user(self):
        tester = User.query.filter_by(first_name='test').first()
        tester.first_name = "Andrew"
        db.session.add(tester)
        db.session.commit()
        self.assertEqual(tester.first_name, "Andrew")

    def test_get_user(self):
        tester = User.query.filter_by(first_name='test').first()
        self.assertEqual(tester.id, 1)