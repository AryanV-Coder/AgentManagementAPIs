#!/bin/bash
# Validation script to check if everything is ready for Keploy integration

echo "🔍 Keploy Integration Readiness Check"
echo "===================================="
echo ""

# Check if OpenAPI schema exists
if [ -f "openapi.json" ]; then
    echo "✅ OpenAPI schema: openapi.json exists"
    # Check if it's valid JSON
    if python -m json.tool openapi.json > /dev/null 2>&1; then
        echo "✅ OpenAPI schema: Valid JSON format"
    else
        echo "❌ OpenAPI schema: Invalid JSON format"
    fi
else
    echo "❌ OpenAPI schema: Missing (run: python generate_openapi.py)"
fi

# Check CI/CD workflow
if [ -f ".github/workflows/ci-cd.yml" ]; then
    echo "✅ CI/CD workflow: Exists"
    
    # Check if Keploy command placeholder is still there
    if grep -q "Please replace this with your actual Keploy test command" .github/workflows/ci-cd.yml; then
        echo "⚠️  CI/CD workflow: Still has placeholder - needs your Keploy command"
    else
        echo "✅ CI/CD workflow: Keploy command appears to be updated"
    fi
    
    # Check if KEPLOY_API_KEY is referenced
    if grep -q "KEPLOY_API_KEY" .github/workflows/ci-cd.yml; then
        echo "✅ CI/CD workflow: KEPLOY_API_KEY referenced"
    else
        echo "❌ CI/CD workflow: KEPLOY_API_KEY not found"
    fi
else
    echo "❌ CI/CD workflow: Missing"
fi

# Check if FastAPI app has OpenAPI documentation
if python -c "
from main import app
schema = app.openapi()
if schema.get('info', {}).get('title'):
    print('✅ FastAPI app: OpenAPI documentation configured')
    print(f'   Title: {schema[\"info\"][\"title\"]}')
    print(f'   Paths: {len(schema.get(\"paths\", {}))} endpoints')
else:
    print('❌ FastAPI app: OpenAPI documentation missing')
" 2>/dev/null; then
    :
else
    echo "❌ FastAPI app: Cannot validate (check imports)"
fi

# Check requirements
if [ -f "requirements.txt" ]; then
    echo "✅ Requirements: requirements.txt exists"
    if grep -q "pytest" requirements.txt; then
        echo "✅ Requirements: pytest included"
    else
        echo "⚠️  Requirements: pytest missing"
    fi
else
    echo "❌ Requirements: requirements.txt missing"
fi

echo ""
echo "📋 Next Steps:"
echo "1. If you see any ❌ or ⚠️, fix those issues first"
echo "2. Follow ./setup_keploy.sh for Keploy dashboard setup"
echo "3. Update the workflow with your actual Keploy command"
echo "4. Add KEPLOY_API_KEY to GitHub secrets"
echo "5. Push to GitHub to trigger the pipeline"
