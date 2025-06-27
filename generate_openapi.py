#!/usr/bin/env python3
"""
Script to generate OpenAPI schema from FastAPI app
"""
import json
from main import app

def generate_openapi_schema():
    """Generate and save OpenAPI schema"""
    openapi_schema = app.openapi()
    
    # Save to JSON file
    with open('openapi.json', 'w') as f:
        json.dump(openapi_schema, f, indent=2)
    
    print("OpenAPI schema generated successfully!")
    print("File saved as: openapi.json")

if __name__ == "__main__":
    generate_openapi_schema()
