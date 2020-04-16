import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Drink, Transaction

manager_token="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpiTUhKeV8zLXFUSjluLW5yVUZZTyJ9.eyJpc3MiOiJodHRwczovL3lwZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTkwZTI5MjE1ZGY4YTBjNTZlNTRlYWUiLCJhdWQiOiJjb2ZmZXNob3AiLCJpYXQiOjE1ODcwNTY0NjIsImV4cCI6MTU4NzE0Mjg2MiwiYXpwIjoiY1M0OTRSRzhIS2RCaHJFT2tPWFBla3loSVFFRXRJREciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJkZWxldGU6dHJhbnNhY3Rpb25zIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJnZXQ6dHJhbnNhY3Rpb25zIiwicGF0Y2g6ZHJpbmtzIiwicGF0Y2g6dHJhbnNhY3Rpb25zIiwicG9zdDpkcmlua3MiLCJwb3N0OnRyYW5zYWN0aW9ucyJdfQ.P58tgvVOHLuU3QdxJ0Qg-0WfGRpUbO8kDnsnGy8M3-_C1MunRZYT063xGJbwPU8YQHALJOt52KUNxYeKiFYNFbznk4NKFVT_XVrvEc5i880SlVJ-Eus0MdgAJ9ShJiVOZ6sI8OxefTlfrflS5mBwPk74Pd09NOR2AnfewR4KeCbcv4XDF7E5LP_XLyAnqXnLMxiEVQ-PLOkw1237fJnQ8DgEuhiVeA4-JgyVjahFqwV6IzUjMHMyh4kIZ45vRgMcKP5UfLhfd5iPg1Uu62Yo3ZRVEMLlbggsn6Fzxza5bPRsHQ5r9m1391NlkCvzTlR4DcVpQKNJ--vLn5EmdRlbxg"
barista_token="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpiTUhKeV8zLXFUSjluLW5yVUZZTyJ9.eyJpc3MiOiJodHRwczovL3lwZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTkwZTM0ZTE1ZGY4YTBjNTZlNTUxMzkiLCJhdWQiOiJjb2ZmZXNob3AiLCJpYXQiOjE1ODcwNTY1MDMsImV4cCI6MTU4NzE0MjkwMywiYXpwIjoiY1M0OTRSRzhIS2RCaHJFT2tPWFBla3loSVFFRXRJREciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0cmFuc2FjdGlvbnMiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOnRyYW5zYWN0aW9ucyIsInBvc3Q6dHJhbnNhY3Rpb25zIl19.guSI9WFf4LVJk2SLmnhMAhz7CWf0kIXYhIm-2meV4ymjtuFXTvgq6SqbQOJLUe_6J2RSoFlb2YdPN-d4kGOMpv9_B3JHlc4QWIY3L7OlXZZ2seS0mLZrQbAJpwQ8YdyCTbhb0J0XqDYNv2CTQqAEWVGmP1VJ6QddciRJaCNAS8wHk8Vshp5yJ2fzyTgP4LZDQHft7yXjsSQ0YLh3OPVuDtitZVfcp4COt3tKGy75kOOfJyEjGxuvR5z8pbH6nAxUfbi7H6VNE992e6H5uomCzIKhJ8m_k_8miY0hoqebwYG7AO83jgz_XCnve-E1BiFdSHyGV-jjPDxNxSyCagZGTg"
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fsnd"
        self.database_path = "postgresql://postgres:1234@localhost:5432/fsnd"
        self.headers_manager = {'Content-Type': 'application/json', 'Authorization': manager_token}
        self.headers_barista = {'Content-Type': 'application/json', 'Authorization': barista_token}        
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

    def test_get_all_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    def test_post_drinks(self):
        res = self.client().post('/drinks', headers=self.headers_manager, json={"name":"root beers","price":1.5,"quantity":10})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_drinks_fail(self):
        res = self.client().post('/drinks', headers=self.headers_barista, json={"name":"root beers","price":1.5,"quantity":10})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)      


    def test_patch_drinks(self):
        res = self.client().patch('/drinks/1', headers=self.headers_manager, json={"name":"fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)          
        self.assertTrue(data['drink'])


    def test_patch_drinks_fail(self):
        res = self.client().patch('/drinks/1', json={"name":"fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)          
      

    def test_patch_drinks_fail(self):
        res = self.client().patch('/drinks/1', json={"name":"fanta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)           

    def test_get_transactions(self):
        res = self.client().get('/transactions',headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)            
        self.assertTrue(data['history'])

    def test_get_transactions_fail(self):
        res = self.client().get('/transactions',headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)         


    def test_post_transactions(self):
        res = self.client().post('/transactions',headers=self.headers_barista,json={"drink_id":1,"quantity":1,"created_at":"2020-04-14"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)            

    def test_post_transactions_fail(self):
        res = self.client().post('/transactions',headers=self.headers_barista,json={"drink_id":1,"quantity":1000000,"created_at":"2020-04-14"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)             

    def test_patch_transactions(self):
        res = self.client().patch('/transactions',headers=self.headers_barista,json={"trans_id":1,"quantity":2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)         

    def test_patch_transactions_fail(self):
        res = self.client().patch('/transactions',headers=self.headers_barista,json={"trans_id":1000000,"quantity":2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)  

    def test_popular_transactions(self):
        res = self.client().get('/transactions/popular',headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)  
        self.assertTrue(data['toplist'])

    def test_popular_transactions_fail(self):
        res = self.client().post('/transactions/popular',headers=self.headers_barista)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)  
 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
