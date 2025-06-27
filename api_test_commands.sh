#!/bin/bash
# Curl commands for testing Agent Management API

BASE_URL="http://localhost:8000"

echo "=== Agent Management API Test Commands ==="
echo ""

echo "1. Create a new agent:"
echo "curl -X POST \"$BASE_URL/agent/\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"codename\": \"bond\", \"password\": \"007\", \"description\": \"Secret agent\"}'"
echo ""

echo "2. Get an agent:"
echo "curl -X GET \"$BASE_URL/agent/bond/007\""
echo ""

echo "3. Update an agent:"
echo "curl -X PUT \"$BASE_URL/agent/\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"codename\": \"bond\", \"password\": \"007\", \"description\": \"Updated secret agent\"}'"
echo ""

echo "4. Delete an agent:"
echo "curl -X DELETE \"$BASE_URL/agent/bond/007\""
echo ""

echo "5. Get API documentation:"
echo "curl -X GET \"$BASE_URL/docs\""
echo ""

echo "6. Get OpenAPI schema:"
echo "curl -X GET \"$BASE_URL/openapi.json\""
