#!/bin/bash
# Keploy Setup Helper Script

echo "🤖 Keploy API Testing Setup Helper"
echo "=================================="
echo ""

echo "📋 Steps to complete Keploy integration:"
echo ""

echo "1. 🌐 Go to Keploy Dashboard:"
echo "   https://app.keploy.io/"
echo ""

echo "2. 📁 Create/Select your project"
echo ""

echo "3. 📄 Upload your OpenAPI schema:"
echo "   File: openapi.json (already generated in this directory)"
echo ""

echo "4. 🧪 Go to Test Suite section in sidebar"
echo ""

echo "5. 🏃 Click 'Run test suites natively'"
echo ""

echo "6. 📋 Copy the command that looks like:"
echo "   For CI/CD testing: keploy test-suite --app=YOUR_APP_ID --base-path http://localhost:8000 --cloud"
echo "   For production testing: keploy test-suite --app=YOUR_APP_ID --base-path https://agentmanagementapis.onrender.com --cloud"
echo "   (Recommend using localhost for CI/CD pipeline)"
echo ""

echo "7. 🔑 Get your API key from account settings"
echo ""

echo "8. 🔒 Add to GitHub Secrets (Settings → Security → Actions):"
echo "   - KEPLOY_API_KEY: your_api_key_here"
echo ""

echo "9. ✏️  Update .github/workflows/ci-cd.yml:"
echo "   - Replace the placeholder command with your actual Keploy command"
echo "   - For CI/CD: Use http://localhost:8000 as base-path"
echo "   - For production testing: Use https://agentmanagementapis.onrender.com"
echo ""

echo "10. 🚀 Push to GitHub to trigger the pipeline"
echo ""

echo "📊 Generated files for Keploy:"
ls -la openapi.json 2>/dev/null && echo "✅ openapi.json (ready for upload)" || echo "❌ openapi.json not found - run: python generate_openapi.py"

echo ""
echo "🎯 Next: Follow the steps above, then push your changes to GitHub!"
