import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from models.input import Input_For_Post_And_Put
import db

client = TestClient(app)

# --- UNIT TESTS ---
class TestAgentLogic(unittest.TestCase):
    @patch('main.collection')
    def test_get_agent_found(self, mock_collection):
        mock_collection.find_one.return_value = {'_id': '1', 'codename': 'bond', 'password': '007', 'description': 'spy'}
        response = client.get('/agent/bond/007')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['codename'], 'bond')

    @patch('main.collection')
    def test_get_agent_not_found(self, mock_collection):
        mock_collection.find_one.return_value = None
        response = client.get('/agent/ghost/000')
        self.assertEqual(response.status_code, 404)

    @patch('main.collection')
    def test_create_agent_success(self, mock_collection):
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.return_value.inserted_id = '123abc'
        data = {"codename": "new", "password": "pass", "description": "desc"}
        response = client.post('/agent/', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

    @patch('main.collection')
    def test_create_agent_conflict(self, mock_collection):
        mock_collection.find_one.return_value = {'codename': 'bond'}
        data = {"codename": "bond", "password": "007", "description": "spy"}
        response = client.post('/agent/', json=data)
        self.assertEqual(response.status_code, 409)

    @patch('main.collection')
    def test_delete_agent_success(self, mock_collection):
        mock_collection.delete_one.return_value.deleted_count = 1
        response = client.delete('/agent/bond/007')
        self.assertEqual(response.status_code, 200)

    @patch('main.collection')
    def test_delete_agent_not_found(self, mock_collection):
        mock_collection.delete_one.return_value.deleted_count = 0
        response = client.delete('/agent/ghost/000')
        self.assertEqual(response.status_code, 404)

    @patch('main.collection')
    def test_update_agent_success(self, mock_collection):
        mock_collection.update_one.return_value.matched_count = 1
        data = {"codename": "bond", "password": "007", "description": "updated"}
        response = client.put('/agent/', json=data)
        self.assertEqual(response.status_code, 200)

    @patch('main.collection')
    def test_update_agent_not_found(self, mock_collection):
        mock_collection.update_one.return_value.matched_count = 0
        data = {"codename": "ghost", "password": "000", "description": "none"}
        response = client.put('/agent/', json=data)
        self.assertEqual(response.status_code, 404)

# --- INTEGRATION TESTS (Non-mocking, real DB) ---
class TestAgentIntegration(unittest.TestCase):
    def setUp(self):
        self.test_agent = {"codename": "inttest", "password": "intpass", "description": "integration"}
        db.collection.delete_many({"codename": self.test_agent["codename"]})

    def tearDown(self):
        db.collection.delete_many({"codename": self.test_agent["codename"]})

    def test_create_and_get_agent(self):
        response = client.post('/agent/', json=self.test_agent)
        self.assertEqual(response.status_code, 201)
        response = client.get(f'/agent/{self.test_agent["codename"]}/{self.test_agent["password"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['codename'], self.test_agent['codename'])

    def test_update_agent(self):
        client.post('/agent/', json=self.test_agent)
        update = self.test_agent.copy()
        update['description'] = 'updated'
        response = client.put('/agent/', json=update)
        self.assertEqual(response.status_code, 200)
        agent = db.collection.find_one({"codename": update['codename']})
        self.assertEqual(agent['description'], 'updated')

    def test_delete_agent(self):
        client.post('/agent/', json=self.test_agent)
        response = client.delete(f'/agent/{self.test_agent["codename"]}/{self.test_agent["password"]}')
        self.assertEqual(response.status_code, 200)
        agent = db.collection.find_one({"codename": self.test_agent['codename']})
        self.assertIsNone(agent)

# --- API TESTS ---
def test_api_endpoints():
    agent = {"codename": "apitest", "password": "apipass", "description": "api"}
    # Clean up before
    db.collection.delete_many({"codename": agent["codename"]})
    # Create
    r = client.post('/agent/', json=agent)
    assert r.status_code == 201
    # Get
    r = client.get(f'/agent/{agent["codename"]}/{agent["password"]}')
    assert r.status_code == 200
    # Update
    agent['description'] = 'api updated'
    r = client.put('/agent/', json=agent)
    assert r.status_code == 200
    # Delete
    r = client.delete(f'/agent/{agent["codename"]}/{agent["password"]}')
    assert r.status_code == 200
    # Clean up after
    db.collection.delete_many({"codename": agent["codename"]})

def run_coverage():
    import subprocess
    print("\nRunning coverage analysis...")
    subprocess.run(['coverage', 'run', '--source=main,db,models', '-m', 'unittest', 'discover', '-s', '.', '-p', 'tests.py'])
    subprocess.run(['coverage', 'report', '-m'])

if __name__ == "__main__":
    unittest.main()
