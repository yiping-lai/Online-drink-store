import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Drink, Transaction

manager_token = os.environ['MANAGER_TOKEN']
barista_token = os.environ['BARISTA_TOEKN']

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fsnd"
        self.database_path = "postgresql://postgres:1234@localhost:5432/fsnd"
        self.headers_manager = {
            'Content-Type': 'application/json',
            'Authorization': manager_token}
        self.headers_barista = {
            'Content-Type': 'application/json',
            'Authorization': barista_token}
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_drinks(self):
        res = self.client().post(
            '/drinks',
            headers=self.headers_manager,
            json={
                "name": "root beers",
                "price": 1.5,
                "quantity": 10})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_drinks_fail(self):
        res = self.client().post(
            '/drinks',
            headers=self.headers_barista,
            json={
                "name": "root beers",
                "price": 1.5,
                "quantity": 10})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_get_all_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    def test_patch_drinks(self):
        res = self.client().patch(
            '/drinks/1',
            headers=self.headers_manager,
            json={
                "name": "fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drink'])

    def test_patch_drinks_fail(self):
        res = self.client().patch('/drinks/1', json={"name": "fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_drinks_fail(self):
        res = self.client().patch('/drinks/1', json={"name": "fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_transactions(self):
        res = self.client().post(
            '/transactions',
            headers=self.headers_barista,
            json={
                "drink_id": 1,
                "quantity": 1,
                "created_at": "2020-04-14"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_transactions_fail(self):
        res = self.client().post(
            '/transactions',
            headers=self.headers_barista,
            json={
                "drink_id": 1,
                "quantity": 1000000,
                "created_at": "2020-04-14"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_transactions(self):
        res = self.client().get('/transactions', headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['history'])

    def test_get_transactions_fail(self):
        res = self.client().get('/transactions', headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_transactions(self):
        res = self.client().patch(
            '/transactions',
            headers=self.headers_barista,
            json={
                "trans_id": 1,
                "quantity": 2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_transactions_fail(self):
        res = self.client().patch(
            '/transactions',
            headers=self.headers_barista,
            json={
                "trans_id": 1000000,
                "quantity": 2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_popular_transactions(self):
        res = self.client().get('/transactions/popular', headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['toplist'])

    def test_popular_transactions_fail(self):
        res = self.client().post('/transactions/popular', headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
