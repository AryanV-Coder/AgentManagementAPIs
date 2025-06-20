# Agent Management API

A FastAPI-based RESTful API for managing agent records, using MongoDB Atlas as the backend database. This API allows you to create, retrieve, update, and delete agent records securely.

## Database
- **Type:** MongoDB Atlas (cloud-hosted)
- **Integration:** The server connects to MongoDB Atlas using the `pymongo` library and the `certifi` package for SSL certificate verification. The connection is established in `db.py`:
  ```python
  from pymongo.mongo_client import MongoClient
  from pymongo.server_api import ServerApi
  import certifi
  uri = "<your-mongodb-uri>"
  client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
  db = client.agents_db
  collection = db['agents_data']
  ```

## API Endpoints

### 1. Get Agent by Codename and Password
- **Endpoint:** `/agent/{codename}/{password}`
- **Method:** GET
- **Description:** Retrieve agent details by codename and password.
- **Sample Request:**
  ```http
  GET /agent/jamesbond/secret123
  ```
- **Sample Response:**
  ```json
  {
    "_id": "60f7c2e2e1b1c8a1b8e4d123",
    "codename": "jamesbond",
    "password": "secret123",
    "description": "MI6 Agent"
  }
  ```

### 2. Create Agent
- **Endpoint:** `/agent/`
- **Method:** POST
- **Description:** Create a new agent. Codename must be unique.
- **Request Body:**
  ```json
  {
    "codename": "jamesbond",
    "password": "secret123",
    "description": "MI6 Agent"
  }
  ```
- **Sample Response:**
  ```json
  {
    "status_code": 201,
    "id": "60f7c2e2e1b1c8a1b8e4d123"
  }
  ```
- **Error (Duplicate):**
  ```json
  {
    "detail": "Agent with this codename already exists.",
    "status_code": 409
  }
  ```

### 3. Update Agent
- **Endpoint:** `/agent/`
- **Method:** PUT
- **Description:** Update an agent's details. Requires correct codename and password in the body.
- **Request Body:**
  ```json
  {
    "codename": "jamesbond",
    "password": "secret123",
    "description": "Updated MI6 Agent"
  }
  ```
- **Sample Response:**
  ```json
  {
    "status_code": 200,
    "detail": "Agent updated successfully."
  }
  ```
- **Error (Not Found):**
  ```json
  {
    "detail": "Agent not found or password incorrect.",
    "status_code": 404
  }
  ```

### 4. Delete Agent
- **Endpoint:** `/agent/{codename}/{password}`
- **Method:** DELETE
- **Description:** Delete an agent by codename and password.
- **Sample Request:**
  ```http
  DELETE /agent/jamesbond/secret123
  ```
- **Sample Response:**
  ```json
  {
    "status_code": 200,
    "detail": "Agent deleted successfully."
  }
  ```
- **Error (Not Found):**
  ```json
  {
    "detail": "Agent not found or password incorrect.",
    "status_code": 404
  }
  ```

## How to Run the Server

### Option 1: Use my Deployed APIs on Postman
- My Render Url - https://agentmanagementapis.onrender.com
- Use Postman to send requests directly to my Render URL.

### Option 2: Clone and Run Locally
1. **Clone the repository:**
   ```sh
   git clone https://github.com/AryanV-Coder/AgentManagementAPIs.git
   cd AgentManagementAPIs
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your MongoDB Atlas URI in `db.py`.**
4. **Run the server:**
   ```sh
   uvicorn main:app --reload
   ```
5. **Access the API:**
   - Use [Postman](https://www.postman.com/) to send requests to `http://localhost:8000` or Use FastAPI Swagger UI

## Interacting with the API
- Use Postman to test all endpoints.
- Set the request type (GET, POST, PUT, DELETE) and provide the required parameters or body as shown above.
