#!/bin/bash
# Quick API test script

echo "🚀 Starting Agent Management API Test..."

# Start the server in the background
echo "📡 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test if server is running
echo "🔍 Checking if server is running..."
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "✅ Server is running!"
else
    echo "❌ Server failed to start"
    exit 1
fi

# Test API endpoints
echo "🧪 Testing API endpoints..."

echo "1. Testing POST /agent/ (Create agent)"
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/agent/" \
  -H "Content-Type: application/json" \
  -d '{"codename": "testbond", "password": "test007", "description": "Test agent"}')
echo "Response: $CREATE_RESPONSE"

echo "2. Testing GET /agent/{codename}/{password} (Get agent)"
GET_RESPONSE=$(curl -s -X GET "http://localhost:8000/agent/testbond/test007")
echo "Response: $GET_RESPONSE"

echo "3. Testing PUT /agent/ (Update agent)"
UPDATE_RESPONSE=$(curl -s -X PUT "http://localhost:8000/agent/" \
  -H "Content-Type: application/json" \
  -d '{"codename": "testbond", "password": "test007", "description": "Updated test agent"}')
echo "Response: $UPDATE_RESPONSE"

echo "4. Testing DELETE /agent/{codename}/{password} (Delete agent)"
DELETE_RESPONSE=$(curl -s -X DELETE "http://localhost:8000/agent/testbond/test007")
echo "Response: $DELETE_RESPONSE"

echo "5. Testing OpenAPI schema endpoint"
SCHEMA_RESPONSE=$(curl -s http://localhost:8000/openapi.json | jq '.info.title' 2>/dev/null || echo "Schema available")
echo "Schema title: $SCHEMA_RESPONSE"

# Clean up
echo "🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "✅ API test completed!"
